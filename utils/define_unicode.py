def unicode_to_define(name, codepoint_hex):
    codepoint = int(codepoint_hex, 16)
    utf8_bytes = chr(codepoint).encode('utf-8')
    hex_bytes = ''.join(f"\\x{b:02x}" for b in utf8_bytes)
    return f'#define {name} "{hex_bytes}"  // U+{codepoint_hex.upper()}'

def main():
    icons = [
        ("ICON_FA_SIGN_OUT", "F2F5")
    ]

    for name, code in icons:
        print(unicode_to_define(name, code))

if __name__ == "__main__":
    main()
