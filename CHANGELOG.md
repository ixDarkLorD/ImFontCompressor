# Changelog

All notable changes to this project will be documented in this file.

## [1.0.2] - 2025-06-18

### Added

- Unicode Tab: Generate C-style #define macros for named Unicode codepoints.

### Changed

- Tab bar dynamically aligns to the right for RTL languages.
- Simplified layout by removing redundant frames.
- Cleaned up startup configuration and resource handling.
- Updated theme application to more UI elements (labels, frames, outputs).

### Fixed

- UI now properly reflows with RTL alignment across all tabs.
- Button hover/selection state now respects theme consistently after tab switching.
- "**Check for Update**" button now works properly.

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
