#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

// stb_compress* from stb.h - declaration
typedef unsigned int stb_uint;
typedef unsigned char stb_uchar;
stb_uint stb_compress(stb_uchar* out, stb_uchar* in, stb_uint len);

enum SourceEncoding
{
    SourceEncoding_U8,      // New default since 2024/11
    SourceEncoding_U32,
    SourceEncoding_Base85,
};

static bool binary_to_compressed_c(const char* inputfile, const char* symbolname,
                            SourceEncoding source_encoding, bool use_compression,
                            bool use_static, const char* outputfile = nullptr);

static const char* ExtractFilenameWithoutExtension(const char* path);

int main(int argc, char** argv)
{
    if (argc < 2)
    {
        printf("Usage:\n");
        printf("  %s [options] <inputfile> [-output <outputfile>] [symbolname]\n\n", argv[0]);
        printf("Options:\n");
        printf("  -u8        Encode as uint8_t array (default)\n");
        printf("  -u32       Encode as uint32_t array\n");
        printf("  -base85    Encode using base85 encoding\n");
        printf("  -nocompress  Disable compression of input file\n");
        printf("  -nostatic    Do not mark generated symbol as 'static'\n");
        printf("  -output <outputfile>  Path to output .cpp file (defaults to stdout if not set)\n\n");
        printf("Arguments:\n");
        printf("  <inputfile>   Path to the binary file to embed\n");
        printf("  [symbolname]  Optional variable/function name for the embedded data.\n");
        printf("                Defaults to the input file name without extension or path.\n\n");
        printf("Encoding Efficiency:\n");
        printf("  -u8     = ~12 bytes of source per 4 bytes of data. 4 bytes in binary.\n");
        printf("  -u32    = ~11 bytes of source per 4 bytes of data. 4 bytes in binary. Needs endianness swapping on big-endian.\n");
        printf("  -base85 =  ~5 bytes of source per 4 bytes of data. 5 bytes in binary. Requires decoder.\n");
        return 0;
    }

    int argn = 1;
    bool use_compression = true;
    bool use_static = true;
    SourceEncoding source_encoding = SourceEncoding_U8;
    const char* inputfile = nullptr;
    const char* outputfile = nullptr;
    const char* symbolname = nullptr;

    // Parse options first
    while (argn < argc && argv[argn][0] == '-')
    {
        if (strcmp(argv[argn], "-u8") == 0) { source_encoding = SourceEncoding_U8; argn++; }
        else if (strcmp(argv[argn], "-u32") == 0) { source_encoding = SourceEncoding_U32; argn++; }
        else if (strcmp(argv[argn], "-base85") == 0) { source_encoding = SourceEncoding_Base85; argn++; }
        else if (strcmp(argv[argn], "-nocompress") == 0) { use_compression = false; argn++; }
        else if (strcmp(argv[argn], "-nostatic") == 0) { use_static = false; argn++; }
        else break;
    }

    if (argn >= argc) {
        fprintf(stderr, "Missing inputfile.\n");
        return 1;
    }

    inputfile = argv[argn++];

    // Optional [-output <outputfile>]
    if (argn < argc && strcmp(argv[argn], "-output") == 0)
    {
        if (argn + 1 >= argc) {
            fprintf(stderr, "Missing value for -output\n");
            return 1;
        }
        outputfile = argv[argn + 1];
        argn += 2;
    }

    // Optional [symbolname]
    if (argn < argc)
    {
        symbolname = argv[argn++];
    }
    else
    {
        symbolname = ExtractFilenameWithoutExtension(inputfile);
    }

    if (argn < argc)
    {
        fprintf(stderr, "Unexpected argument: '%s'\n", argv[argn]);
        return 1;
    }

    bool ret = binary_to_compressed_c(inputfile, symbolname, source_encoding, use_compression, use_static, outputfile);
    if (!ret)
        fprintf(stderr, "Error processing file: '%s'\n", inputfile);
    return ret ? 0 : 1;
}

char Encode85Byte(unsigned int x)
{
    x = (x % 85) + 35;
    return (char)((x >= '\\') ? x + 1 : x);
}

bool binary_to_compressed_c(const char* inputfile, const char* symbolname,
                            SourceEncoding source_encoding, bool use_compression,
                            bool use_static, const char* outputfile)
{
    // Read file
    FILE* f = fopen(inputfile, "rb");
    if (!f) return false;
    
    int data_sz;
    if (fseek(f, 0, SEEK_END) || (data_sz = (int)ftell(f)) == -1 || fseek(f, 0, SEEK_SET)) {
        fclose(f);
        return false;
    }

    char* data = new char[data_sz + 4];
    if (fread(data, 1, data_sz, f) != (size_t)data_sz) {
        fclose(f);
        delete[] data;
        return false;
    }
    memset(data + data_sz, 0, 4);
    fclose(f);

    // Compress
    int maxlen = data_sz + 512 + (data_sz >> 2) + sizeof(int);
    char* compressed = use_compression ? new char[maxlen] : data;
    int compressed_sz = use_compression ? stb_compress((stb_uchar*)compressed, (stb_uchar*)data, data_sz) : data_sz;
    if (use_compression)
        memset(compressed + compressed_sz, 0, maxlen - compressed_sz);

    // Output
    FILE* out = stdout;
    bool out_opened = false;
    if (outputfile && strlen(outputfile) > 0) {
        out = fopen(outputfile, "w");
        if (!out) {
            fprintf(stderr, "Error: Could not open output file '%s'\n", outputfile);
            if (use_compression)
                delete[] compressed;
            delete[] data;
            return false;
        }
        out_opened = true;
    }

    fprintf(out, "// File: '%s' (%d bytes)\n", inputfile, data_sz);
    const char* static_str = use_static ? "static " : "";
    const char* compressed_str = use_compression ? "compressed_" : "";

    if (source_encoding == SourceEncoding_Base85)
    {
        fprintf(out, "// Exported using binary_to_compressed_c -base85 \"%s\" %s\n", inputfile, symbolname);
        fprintf(out, "%sconst char %s_%sdata_base85[%d+1] =\n    \"", static_str, symbolname, compressed_str, ((compressed_sz + 3) / 4) * 5);
        char prev_c = 0;
        for (int src_i = 0; src_i < compressed_sz; src_i += 4)
        {
            unsigned int d = *(unsigned int*)(compressed + src_i);
            for (unsigned int n5 = 0; n5 < 5; n5++, d /= 85)
            {
                char c = Encode85Byte(d);
                fprintf(out, (c == '?' && prev_c == '?') ? "\\%c" : "%c", c);
                prev_c = c;
            }
            if ((src_i % 112) == 112 - 4)
                fprintf(out, "\"\n    \"");
        }
        fprintf(out, "\";\n\n");
    }
    else if (source_encoding == SourceEncoding_U8)
    {
        fprintf(out, "// Exported using binary_to_compressed_c -u8 \"%s\" %s\n", inputfile, symbolname);
        fprintf(out, "%sconst unsigned int %s_%ssize = %d;\n", static_str, symbolname, compressed_str, compressed_sz);
        fprintf(out, "%sconst unsigned char %s_%sdata[%d] =\n{", static_str, symbolname, compressed_str, compressed_sz);
        int column = 0;
        for (int i = 0; i < compressed_sz; i++)
        {
            if (column == 0)
                fprintf(out, "\n    ");
            column += fprintf(out, "%d,", static_cast<unsigned char>(compressed[i]));
            if (column >= 180)
                column = 0;
        }
        fprintf(out, "\n};\n\n");
    }
    else if (source_encoding == SourceEncoding_U32)
    {
        fprintf(out, "// Exported using binary_to_compressed_c -u32 \"%s\" %s\n", inputfile, symbolname);
        fprintf(out, "%sconst unsigned int %s_%ssize = %d;\n", static_str, symbolname, compressed_str, compressed_sz);
        fprintf(out, "%sconst unsigned int %s_%sdata[%d/4] =\n{", static_str, symbolname, compressed_str, ((compressed_sz + 3) / 4) * 4);
        int column = 0;
        for (int i = 0; i < compressed_sz; i += 4)
        {
            unsigned int d = *(unsigned int*)(compressed + i);
            if ((column++ % 14) == 0)
                fprintf(out, "\n    0x%08x, ", d);
            else
                fprintf(out, "0x%08x, ", d);
        }
        fprintf(out, "\n};\n\n");
    }

    if (out_opened)
        fclose(out);
    delete[] data;
    if (use_compression)
        delete[] compressed;
    return true;
}

const char* ExtractFilenameWithoutExtension(const char* path) {
    const char* filename = strrchr(path, '/');
#ifdef _WIN32
    const char* alt = strrchr(path, '\\');
    if (!filename || (alt && alt > filename))
        filename = alt;
#endif
    filename = filename ? filename + 1 : path;

    // Find the dot before the extension
    size_t len = strlen(filename);
    for (size_t i = 0; i < len; ++i) {
        if (filename[i] == '.') {
            static char buffer[256];
            strncpy(buffer, filename, i);
            buffer[i] = '\0';
            return buffer;
        }
    }

    return filename; // No extension
}

// stb_compress* from stb.h - definition

////////////////////           compressor         ///////////////////////

static stb_uint stb_adler32(stb_uint adler32, stb_uchar *buffer, stb_uint buflen)
{
    const unsigned long ADLER_MOD = 65521;
    unsigned long s1 = adler32 & 0xffff, s2 = adler32 >> 16;
    unsigned long blocklen, i;

    blocklen = buflen % 5552;
    while (buflen) {
        for (i=0; i + 7 < blocklen; i += 8) {
            s1 += buffer[0], s2 += s1;
            s1 += buffer[1], s2 += s1;
            s1 += buffer[2], s2 += s1;
            s1 += buffer[3], s2 += s1;
            s1 += buffer[4], s2 += s1;
            s1 += buffer[5], s2 += s1;
            s1 += buffer[6], s2 += s1;
            s1 += buffer[7], s2 += s1;

            buffer += 8;
        }

        for (; i < blocklen; ++i)
            s1 += *buffer++, s2 += s1;

        s1 %= ADLER_MOD, s2 %= ADLER_MOD;
        buflen -= blocklen;
        blocklen = 5552;
    }
    return (s2 << 16) + s1;
}

static unsigned int stb_matchlen(stb_uchar *m1, stb_uchar *m2, stb_uint maxlen)
{
    stb_uint i;
    for (i=0; i < maxlen; ++i)
        if (m1[i] != m2[i]) return i;
    return i;
}

// simple implementation that just takes the source data in a big block

static stb_uchar *stb__out;
static FILE      *stb__outfile;
static stb_uint   stb__outbytes;

static void stb__write(unsigned char v)
{
    fputc(v, stb__outfile);
    ++stb__outbytes;
}

//#define stb_out(v)    (stb__out ? *stb__out++ = (stb_uchar) (v) : stb__write((stb_uchar) (v)))
#define stb_out(v)    do { if (stb__out) *stb__out++ = (stb_uchar) (v); else stb__write((stb_uchar) (v)); } while (0)

static void stb_out2(stb_uint v) { stb_out(v >> 8); stb_out(v); }
static void stb_out3(stb_uint v) { stb_out(v >> 16); stb_out(v >> 8); stb_out(v); }
static void stb_out4(stb_uint v) { stb_out(v >> 24); stb_out(v >> 16); stb_out(v >> 8 ); stb_out(v); }

static void outliterals(stb_uchar *in, int numlit)
{
    while (numlit > 65536) {
        outliterals(in,65536);
        in     += 65536;
        numlit -= 65536;
    }

    if      (numlit ==     0)    ;
    else if (numlit <=    32)    stb_out (0x000020 + numlit-1);
    else if (numlit <=  2048)    stb_out2(0x000800 + numlit-1);
    else /*  numlit <= 65536) */ stb_out3(0x070000 + numlit-1);

    if (stb__out) {
        memcpy(stb__out,in,numlit);
        stb__out += numlit;
    } else
        fwrite(in, 1, numlit, stb__outfile);
}

static int stb__window = 0x40000; // 256K

static int stb_not_crap(int best, int dist)
{
    return   ((best > 2  &&  dist <= 0x00100)
        || (best > 5  &&  dist <= 0x04000)
        || (best > 7  &&  dist <= 0x80000));
}

static  stb_uint stb__hashsize = 32768;

// note that you can play with the hashing functions all you
// want without needing to change the decompressor
#define stb__hc(q,h,c)      (((h) << 7) + ((h) >> 25) + q[c])
#define stb__hc2(q,h,c,d)   (((h) << 14) + ((h) >> 18) + (q[c] << 7) + q[d])
#define stb__hc3(q,c,d,e)   ((q[c] << 14) + (q[d] << 7) + q[e])

static unsigned int stb__running_adler;

static int stb_compress_chunk(stb_uchar *history,
    stb_uchar *start,
    stb_uchar *end,
    int length,
    int *pending_literals,
    stb_uchar **chash,
    stb_uint mask)
{
    (void)history;
    int window = stb__window;
    stb_uint match_max;
    stb_uchar *lit_start = start - *pending_literals;
    stb_uchar *q = start;

#define STB__SCRAMBLE(h)   (((h) + ((h) >> 16)) & mask)

    // stop short of the end so we don't scan off the end doing
    // the hashing; this means we won't compress the last few bytes
    // unless they were part of something longer
    while (q < start+length && q+12 < end) {
        int m;
        stb_uint h1,h2,h3,h4, h;
        stb_uchar *t;
        int best = 2, dist=0;

        if (q+65536 > end)
            match_max = (stb_uint)(end-q);
        else
            match_max = 65536;

#define stb__nc(b,d)  ((d) <= window && ((b) > 9 || stb_not_crap((int)(b),(int)(d))))

#define STB__TRY(t,p)  /* avoid retrying a match we already tried */ \
    if (p ? dist != (int)(q-t) : 1)                             \
    if ((m = stb_matchlen(t, q, match_max)) > best)     \
    if (stb__nc(m,q-(t)))                                \
    best = m, dist = (int)(q - (t))

        // rather than search for all matches, only try 4 candidate locations,
        // chosen based on 4 different hash functions of different lengths.
        // this strategy is inspired by LZO; hashing is unrolled here using the
        // 'hc' macro
        h = stb__hc3(q,0, 1, 2); h1 = STB__SCRAMBLE(h);
        t = chash[h1]; if (t) STB__TRY(t,0);
        h = stb__hc2(q,h, 3, 4); h2 = STB__SCRAMBLE(h);
        h = stb__hc2(q,h, 5, 6);        t = chash[h2]; if (t) STB__TRY(t,1);
        h = stb__hc2(q,h, 7, 8); h3 = STB__SCRAMBLE(h);
        h = stb__hc2(q,h, 9,10);        t = chash[h3]; if (t) STB__TRY(t,1);
        h = stb__hc2(q,h,11,12); h4 = STB__SCRAMBLE(h);
        t = chash[h4]; if (t) STB__TRY(t,1);

        // because we use a shared hash table, can only update it
        // _after_ we've probed all of them
        chash[h1] = chash[h2] = chash[h3] = chash[h4] = q;

        if (best > 2)
            assert(dist > 0);

        // see if our best match qualifies
        if (best < 3) { // fast path literals
            ++q;
        } else if (best > 2  &&  best <= 0x80    &&  dist <= 0x100) {
            outliterals(lit_start, (int)(q-lit_start)); lit_start = (q += best);
            stb_out(0x80 + best-1);
            stb_out(dist-1);
        } else if (best > 5  &&  best <= 0x100   &&  dist <= 0x4000) {
            outliterals(lit_start, (int)(q-lit_start)); lit_start = (q += best);
            stb_out2(0x4000 + dist-1);
            stb_out(best-1);
        } else if (best > 7  &&  best <= 0x100   &&  dist <= 0x80000) {
            outliterals(lit_start, (int)(q-lit_start)); lit_start = (q += best);
            stb_out3(0x180000 + dist-1);
            stb_out(best-1);
        } else if (best > 8  &&  best <= 0x10000 &&  dist <= 0x80000) {
            outliterals(lit_start, (int)(q-lit_start)); lit_start = (q += best);
            stb_out3(0x100000 + dist-1);
            stb_out2(best-1);
        } else if (best > 9                      &&  dist <= 0x1000000) {
            if (best > 65536) best = 65536;
            outliterals(lit_start, (int)(q-lit_start)); lit_start = (q += best);
            if (best <= 0x100) {
                stb_out(0x06);
                stb_out3(dist-1);
                stb_out(best-1);
            } else {
                stb_out(0x04);
                stb_out3(dist-1);
                stb_out2(best-1);
            }
        } else {  // fallback literals if no match was a balanced tradeoff
            ++q;
        }
    }

    // if we didn't get all the way, add the rest to literals
    if (q-start < length)
        q = start+length;

    // the literals are everything from lit_start to q
    *pending_literals = (int)(q - lit_start);

    stb__running_adler = stb_adler32(stb__running_adler, start, (stb_uint)(q - start));
    return (int)(q - start);
}

static int stb_compress_inner(stb_uchar *input, stb_uint length)
{
    int literals = 0;
    stb_uint len,i;

    stb_uchar **chash;
    chash = (stb_uchar**) malloc(stb__hashsize * sizeof(stb_uchar*));
    if (chash == nullptr) return 0; // failure
    for (i=0; i < stb__hashsize; ++i)
        chash[i] = nullptr;

    // stream signature
    stb_out(0x57); stb_out(0xbc);
    stb_out2(0);

    stb_out4(0);       // 64-bit length requires 32-bit leading 0
    stb_out4(length);
    stb_out4(stb__window);

    stb__running_adler = 1;

    len = stb_compress_chunk(input, input, input+length, length, &literals, chash, stb__hashsize-1);
    assert(len == length);

    outliterals(input+length - literals, literals);

    free(chash);

    stb_out2(0x05fa); // end opcode

    stb_out4(stb__running_adler);

    return 1; // success
}

stb_uint stb_compress(stb_uchar *out, stb_uchar *input, stb_uint length)
{
    stb__out = out;
    stb__outfile = nullptr;

    stb_compress_inner(input, length);

    return (stb_uint)(stb__out - out);
}