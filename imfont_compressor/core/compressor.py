import subprocess
import os
from imfont_compressor.core.utils import get_resource_path

def run_compression(params, status_callback):
    font_path = params["font_path"]
    symbol_name = params["symbol_name"] or "data"
    encoding = params["encoding"]
    disable_compression = params["disable_compression"]
    no_static = params["no_static"]
    header_output = params["header_output"]

    if not os.path.isfile(font_path):
        return {"success": False, "error": "Font file not found."}

    output_dir = os.path.dirname(font_path)
    if not os.path.isdir(output_dir):
        return {"success": False, "error": "Output folder is invalid."}

    exe_path = get_resource_path("data", "binary_to_compressed_c.exe")
    if not os.path.isfile(exe_path):
        return {"success": False, "error": "Compressor executable not found."}

    filename = os.path.splitext(os.path.basename(font_path))[0]
    output_file = os.path.join(output_dir, filename + (".h" if header_output else ".cpp"))

    args = [exe_path, encoding]
    if disable_compression:
        args.append("-nocompress")
    if no_static:
        args.append("-nostatic")

    args.append(font_path)
    args.append(symbol_name)

    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        output_text = result.stdout

        if not output_text.strip():
            return {"success": False, "error": "No output from compressor."}

        return {
            "success": True,
            "output_text": output_text,
            "output_file": output_file
        }

    except subprocess.CalledProcessError as e:
        err_msg = e.stderr.strip() if e.stderr else e.stdout.strip() if e.stdout else "Compression failed."
        return {"success": False, "error": err_msg}
    except Exception as e:
        return {"success": False, "error": str(e)}