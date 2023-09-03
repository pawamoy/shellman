# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [1.0.0](https://github.com/pawamoy/shellman/releases/tag/1.0.0) - 2023-09-03

<small>[Compare with 0.4.1](https://github.com/pawamoy/shellman/compare/0.4.1...1.0.0)</small>

It has been a long time since the last release, and the last time I worked on this project.
I've updated the project with my latest template. Support for Python 2 is dropped.
I took the opportunity to privatize most of the API. I'll see in a later version
if there is a need to expose a main `parse` function or similar, to extract
information from a given file.

### Breaking Changes

- `shellman.reader.DocLine.doc_type`: Public object points to a different kind of object: function -> attribute
- `shellman.reader.preprocess_stream`: Public object was removed
- `shellman.reader.preprocess_lines`: Public object was removed
- `shellman.reader.process_blocks`: Public object was removed
- `shellman.reader.merge`: Public object was removed
- `shellman.context.get_cli_context`: Public object was removed
- `shellman.context.get_env_context`: Public object was removed
- `shellman.context.get_file_context`: Public object was removed
- `shellman.context.get_context`: Public object was removed
- `shellman.context.update`: Public object was removed
- `shellman.cli.get_context`: Public object was removed
- `shellman.cli.update`: Public object was removed
- `shellman.cli.merge`: Public object was removed
- `shellman.cli.valid_file`: Public object was removed
- `shellman.cli.render`: Public object was removed
- `shellman.cli.write`: Public object was removed
- `shellman.cli.common_ancestor`: Public object was removed
- `shellman.cli.is_format_string`: Public object was removed
- `shellman.cli.guess_filename`: Public object was removed
- `shellman.cli.output_name_variables`: Public object was removed
- `shellman.cli.get_vcs_root`: Public object was removed
- `shellman.cli.main(argv)`: Parameter was removed
- `shellman.templates.get_builtin_path`: Public object was removed
- `shellman.templates.get_env`: Public object was removed
- `shellman.templates.get_custom_template`: Public object was removed
- `shellman.templates.load_plugin_templates`: Public object was removed
- `shellman.templates.names`: Public object was removed
- `shellman.templates.parser_choices`: Public object was removed
- `shellman.templates.filters.do_groffauto(escape)`: Parameter kind was changed: positional or keyword -> keyword-only
- `shellman.templates.filters.do_smartwrap(indentfirst)`: Parameter kind was changed: positional or keyword -> keyword-only
- `shellman.templates.filters.do_format(string)`: Parameter was added as required
- `shellman.templates.filters.do_groupby(sort)`: Parameter kind was changed: positional or keyword -> keyword-only

### Bug Fixes

- Update for Python 3 and new versions of dependencies ([e16c46f](https://github.com/pawamoy/shellman/commit/e16c46f0a72c8161d745851182379a53f78f242e) by Timothée Mazzucotelli).

### Code Refactoring

- Rewrite tag classes as dataclasses ([f1780d4](https://github.com/pawamoy/shellman/commit/f1780d473ae9a25b52e49614cfc8a866024bcaf7) by Timothée Mazzucotelli).

## [0.4.1](https://github.com/pawamoy/shellman/tags/0.4.1) - 2018-10-10

<small>[Compare with 0.4.0](https://github.com/pawamoy/shellman/compare/0.4.0...0.4.1)</small>

### Fixed
- Fix `body` filter for Python 2 ([ce7d0ef](https://github.com/pawamoy/shellman/commit/ce7d0ef1a4b6f7365580d06ff064504c38247d01)).

## [0.4.0](https://github.com/pawamoy/shellman/tags/0.4.0) - 2018-09-28

<small>[Compare with 0.3.4](https://github.com/pawamoy/shellman/compare/0.3.4...0.4.0)</small>

### Added
- Add context variable to avoid escaping lines starting with given values ([742e023](https://github.com/pawamoy/shellman/commit/742e02321de656e80944d627a6cf727cbc6e66e0)).
- Add usagetext template ([a7c20fc](https://github.com/pawamoy/shellman/commit/a7c20fc751990c229018fc1b6c01835f9da5c193)).

### Fixed
- Fix escape filter condition ([f32cd43](https://github.com/pawamoy/shellman/commit/f32cd43a0b4d88f841e7e5fee9633f7f772637e8)).
- Fix python 2 unicode decode error ([0040028](https://github.com/pawamoy/shellman/commit/0040028f245586bbdffe62b14218abc31539dc85)).
- Fix variables for output ([01155fb](https://github.com/pawamoy/shellman/commit/01155fbf3fcb4c1beb3ad867a428783ae647af57)).

### Misc
- Improve error messages ([96ebb68](https://github.com/pawamoy/shellman/commit/96ebb68c01b7b132666bb900d7f20f2f1c296d65)).

## [0.3.4](https://github.com/pawamoy/shellman/tags/0.3.4) - 2018-09-22

<small>[Compare with 0.3.3](https://github.com/pawamoy/shellman/compare/0.3.3...0.3.4)</small>

### Fixed
- Fix writing UTF-8 contents to file for Python 2 ([9e99b23](https://github.com/pawamoy/shellman/commit/9e99b232d2c1171c9e3ee3b20f0f788b82d1d634)).

### Misc
- Improve credits line ([f7a7cae](https://github.com/pawamoy/shellman/commit/f7a7cae8e1bf7363a73c127b542584e348dfae5c)).

## [0.3.3](https://github.com/pawamoy/shellman/tags/0.3.3) - 2018-09-18

<small>[Compare with 0.3.2](https://github.com/pawamoy/shellman/compare/0.3.2...0.3.3)</small>

### Fixed
- Fix manifest (missing setup.py) ([62ccfaf](https://github.com/pawamoy/shellman/commit/62ccfaf90c4bd301c625101763462bc0c5374567)).

## [0.3.2](https://github.com/pawamoy/shellman/tags/0.3.2) - 2018-09-18

<small>[Compare with 0.3.1](https://github.com/pawamoy/shellman/compare/0.3.1...0.3.2)</small>

### Misc
- Add logo and demo.svg to fix PyPI page ([1e06662](https://github.com/pawamoy/shellman/commit/1e066626e7bcfb919e4d0ce4508b9305a962551a)).

## [0.3.1](https://github.com/pawamoy/shellman/tags/0.3.1) - 2018-09-18

<small>[Compare with 0.3.0](https://github.com/pawamoy/shellman/compare/0.3.0...0.3.1)</small>

### Misc
- Reduce size of package, simplify manifest ([f123b53](https://github.com/pawamoy/shellman/commit/f123b53fc973e05db36f5370d48647d56c571dcf)).
- Switch documents to markdown ([f3917e9](https://github.com/pawamoy/shellman/commit/f3917e9c46566898681e075bbc45afb7151e015f)).

## [0.3.0](https://github.com/pawamoy/shellman/tags/0.3.0) - 2018-09-17

<small>[Compare with 0.2.2](https://github.com/pawamoy/shellman/compare/0.2.2...0.3.0)</small>

### Added
- Add credits in wikipage template ([e70b7c8](https://github.com/pawamoy/shellman/commit/e70b7c8fa4acef2acf1bd7a0dfd96383ef50fec4)).
- Add groupby_unsorted filter to improve option rendering ([2e42177](https://github.com/pawamoy/shellman/commit/2e421776319e8422ddf3191c98666e4c43e1ae16)).
- Add logo ([f9289a0](https://github.com/pawamoy/shellman/commit/f9289a0edbdc53ea16bfbc07bf4ac873ae8548f0)).
- Add new reader module ([ea13cfb](https://github.com/pawamoy/shellman/commit/ea13cfb4a31f9cee2f1a108fd9e1103cb5afda28)).
- Add option to smart_width to indent first line or not ([e625afb](https://github.com/pawamoy/shellman/commit/e625afbe1ba9a851bed40e4792d6fcd0e9fafab1)).
- Add vcsroot name variable ([f5db3b3](https://github.com/pawamoy/shellman/commit/f5db3b35f953a82eba64fc375e4f4638457b1e03)).

### Changed
- Change README.rst to README.md ([4628e76](https://github.com/pawamoy/shellman/commit/4628e76bce717ea3ab47b7f29114caa7e1d50084)).

### Fixed
- Fix code block ([de304ee](https://github.com/pawamoy/shellman/commit/de304eeb56ae2d3431ab6c5db9fdca7100ee2dbd)).
- Fix credits and readme url to gitlab plugins doc ([9958019](https://github.com/pawamoy/shellman/commit/9958019791d981ea566a1973c4f8aa47ae2d5ac2)).
- Fix get context from env ([f1e2296](https://github.com/pawamoy/shellman/commit/f1e2296646ecf523c559e7db3bdcd14779dd01fd)).
- Fix usage tag ([4a47431](https://github.com/pawamoy/shellman/commit/4a474311f748f70a07fceb8acfbabdaba634b3eb)).
- Fix wikipage template ([2f5a0ad](https://github.com/pawamoy/shellman/commit/2f5a0adf3ec8a28c242d1bcad426030fda9ac224)).

### Removed
- Remove blank line in AUTHORS ([e414282](https://github.com/pawamoy/shellman/commit/e414282316518aa2a5f8895433f576d659720195)).
- Remove formatter options, enforce user behavior ([48c26d0](https://github.com/pawamoy/shellman/commit/48c26d03e328272b1001134c86be6d79e1736a90)).
- Remove MPL2.0 notices in sources (now ISC) ([87e92df](https://github.com/pawamoy/shellman/commit/87e92df8b9577968db090ac00bada17086368574)).
- Remove pyup file, remove option-description subtag (implicit) ([4a08fa1](https://github.com/pawamoy/shellman/commit/4a08fa1e42f5972cf462419f7869db6f9a5aafd9)).

### Misc
- Allow failure for style and spell on travis ([4a7a60f](https://github.com/pawamoy/shellman/commit/4a7a60f208dcd654b7f9618b0157ffa584be3bea)).
- Automatically compute indent_str from indent, cast indent to int ([0a09554](https://github.com/pawamoy/shellman/commit/0a0955499450aa5c4069b5fafc38abc0db409094)).
- Handle multiple file input/output, fix some templates vars, format with black ([2c6672b](https://github.com/pawamoy/shellman/commit/2c6672b47b04082865528e6028dd1fd3645c7058)).
- Ignore bandit warning as irrelevant (no html templates) ([4947fe5](https://github.com/pawamoy/shellman/commit/4947fe59d912a954e775944f40da2be94dc095da)).
- Implement context abilities ([5e7c9d4](https://github.com/pawamoy/shellman/commit/5e7c9d4bcc3ddc52caca079a625a927959853843)).
- Implement plugin abilities ([cd4723f](https://github.com/pawamoy/shellman/commit/cd4723f84771d2d5f60fd0dc047d597b708a1c31)).
- Implement smart_width for text format, write more templates ([bb15f51](https://github.com/pawamoy/shellman/commit/bb15f518085c903033b8f9c007c67aba97db03da)).
- Improve helptext usage display, fix smartwrap indent ([11f78bf](https://github.com/pawamoy/shellman/commit/11f78bfcfb043fadc943ac60147293d74c6088d9)).
- Improve manpage groff template, fix various issues ([b829593](https://github.com/pawamoy/shellman/commit/b82959337e7f3c6801533c02976e74f55e268ff9)).
- Link up with argparse ([12f186d](https://github.com/pawamoy/shellman/commit/12f186dd1905f270fc095ff1539d0416d8911afc)).
- Rename tag to section ([5e80735](https://github.com/pawamoy/shellman/commit/5e80735f7f23c2dc9ca63dca94286f0a8763272b)).
- Update demo script and svg ([ec0c282](https://github.com/pawamoy/shellman/commit/ec0c282b282cf23fc97b2767928109d19df37f6d)).
- Update docs, simplify context usage ([8c6c950](https://github.com/pawamoy/shellman/commit/8c6c950f14f2b3f8502e16f2e9ff0fe209b00259)).
- Use GitLab-CI instead of Travis ([de662d0](https://github.com/pawamoy/shellman/commit/de662d03c8b4ee7cb4a35c2b1909da6415de597d)).


## [0.2.2](https://github.com/pawamoy/shellman/tags/0.2.2) - 2017-05-02

<small>[Compare with 0.2.1](https://github.com/pawamoy/shellman/compare/0.2.1...0.2.2)</small>

### Changed
- Change license from MPL 2.0 to ISC (no 'same license' condition) ([868b89e](https://github.com/pawamoy/shellman/commit/868b89ee7df7af36fdc3e4ce424a241867e89c24)).

### Fixed
- Fix cli main return None -> 0 ([7beeecc](https://github.com/pawamoy/shellman/commit/7beeeccb559606bb2b338f2426fb3f5b91f840e7)).
- Fix codacy badge ([fe55efb](https://github.com/pawamoy/shellman/commit/fe55efbd2cd205df1f9b1ce8b02f2dd2d101ba6e)).
- Fix docs spelling ([69988a2](https://github.com/pawamoy/shellman/commit/69988a2e70e18108525ce6bf412cb743441b3516)).
- Fix installation instruction (--user does not install entry point...) ([aa2037b](https://github.com/pawamoy/shellman/commit/aa2037b627ce2e6e2fb1b83fa1fb0669545756ec)).
- Fix man synopsis section ([d79db9a](https://github.com/pawamoy/shellman/commit/d79db9a2c0e361374b1d8e8e376d95599605e9a0)).

### Misc
- Begin to fix output option ([f1e5488](https://github.com/pawamoy/shellman/commit/f1e5488f997a065d26c5f20d00afd7efe93e234d)).
- Hide sphinx warnings, travis install enchant ([c216c78](https://github.com/pawamoy/shellman/commit/c216c780a3502b795bf96a3269f263aeac2c1a08)).
- Use codacy instead of codecov ([c024b1c](https://github.com/pawamoy/shellman/commit/c024b1ce8bfaf0aa7f0d71378d528cebd8e96c46)).


## [0.2.1](https://github.com/pawamoy/shellman/tags/0.2.1) - 2016-12-06

<small>[Compare with 0.2.0](https://github.com/pawamoy/shellman/compare/0.2.0...0.2.1)</small>

### Misc
- Update README, fix help display ([a131b82](https://github.com/pawamoy/shellman/commit/a131b82d84d68e4dfa5211cdc5dd26c930fa33c1)).


## [0.2.0](https://github.com/pawamoy/shellman/tags/0.2.0) - 2016-12-06

<small>[Compare with first commit](https://github.com/pawamoy/shellman/compare/7c77c2bda82a2808aacc4500e01b33f082325ec5...0.2.0)</small>

### Added
- Add check feature, add tests ([4916b51](https://github.com/pawamoy/shellman/commit/4916b514b85fcf6a87a81fe0d3ac6ed4f8bc1011)).
- Add demo example ([ec78d6b](https://github.com/pawamoy/shellman/commit/ec78d6bc2c238c02685e260494be37a510d0f015)).
- Add markdown format, improve python3 compatibility, add gitignore ([6b8c295](https://github.com/pawamoy/shellman/commit/6b8c2959e340bd999177b99c4f1a70286a19aaab)).
- Add tests ([4d08087](https://github.com/pawamoy/shellman/commit/4d080877799e33fba2b8a5ee0133257763ac80c2)).

### Fixed
- Fix changing release date over upstream update ([11738c4](https://github.com/pawamoy/shellman/commit/11738c4484efae0535aa97abd77911752d8d4f47)).
- Fix command line usage and tests usage combination ([bcef7c9](https://github.com/pawamoy/shellman/commit/bcef7c9b5413584c740de2c028f0786e3c8ef48a)).
- Fix dangerous warning about sys.argv as default value ([effe263](https://github.com/pawamoy/shellman/commit/effe26350d8a0516a890c265b195089f83a7fda0)).

### Misc
- Implement new structure ([40b4806](https://github.com/pawamoy/shellman/commit/40b48063b02b5cae1c7074f0921b411fb2aed9f6)).
- Setup tests ([5d50692](https://github.com/pawamoy/shellman/commit/5d50692ab5c49644039eab74d467335fded253c0)).
- Write doc ([1a8e0e4](https://github.com/pawamoy/shellman/commit/1a8e0e4d4624d8ca0eeb66dd78eb3d8b65a11f45)).
