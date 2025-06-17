# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2025-06-17

### Fixed

- Corrected text alignment handling for left-to-right (LTR) and right-to-left (RTL) languages.
- UI elements now dynamically adjust based on the selected language's alignment settings.
- Prevented unnecessary restart prompts when re-selecting the current language.

## [1.0.0] - 2025-06-15

### Added

- Initial release of ImFont Compressor.
- Support for compressing TTF and OTF fonts.
- Multiple encoding options: Unsigned 8-bit (`-u8`), Unsigned 32-bit (`-u32`), Base85 Encoded (`-base85`).
- Options to disable compression and toggle static output.
- Export compressed fonts as C header files (`.h`).
- Drag and drop support for easy font file input.
- Copy compressed output to clipboard or save to file.
- Multiple UI themes for user customization.
- VSCode project configuration and build script using PyInstaller.
