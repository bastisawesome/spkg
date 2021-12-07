# Contributing to SPKG
## Reporting Bugs
### Before Reporting a Bug
- Check the [issues](https://github.com/bastisawesome/spkg/issues) page to see
if a bug has already been reported. If an issue has already been posted, please
do any of the following:
    - Add a comment if you feel like a report is missing something.
    - React to the original comment with a thumbs up.
    - Please do not add comments like "+1" or "I'm also having this issue". It
is more beneficial to keep responses on-topic and concise.
- Ensure the issue is with the latest released version.
- Check the latest milestones and projects to see if the issue is already being
resolved.
- Check the [discussions](https://github.com/bastisawesome/spkg/discussions) to
see if anyone has mentioned related issues.

### Submitting a Good Bug Report
Bug reports are tracked using GitHub's built-in
[issues](https://github.com/bastisawesome/spkg/issues) page. If you've already
confirmed the issue [#beforereportingabug](does not exist), create a new issue.
Issues should include the following:
- Short and concise title explaining the issue.
- Detailed information about what caused the crash, including:
    - What subcommand was used
    - Passed options
    - Package names or expressions used.
    - Operating system information:
        - OS name
        - OS version
    - Python version (`python --version`)
- If the issue is due to a crash, include the crash log generated.
    - Be sure to use Markdown formatting for crash reports, for example, code
blocks.
    - Include the version of Python running!
- If the issue is with particular behaviour, describe the expected behaviour and
the actual results.
- If the issue is related to any existing (opened or closed) issues, but is not
caused by those issues, be sure to link them in your issue.

Bug reports should be detailed but concise, do not report multiple bugs in a
single issue. If you notice multiple bugs, open an independent issue report for
each bug separately. If they are related, be sure to reference the related
issue reports.

## Suggesting Enhancements
### Before Suggesting an Enhancement
- Check the [issues](https://github.com/bastisawesome/spkg/issues) and
[discussions](https://github.com/bastisawesome/spkg/discussions) pages to see
if anyone else has suggested the enhancement. If it has already been post,
please do any of the following:
    - Add a response if you have something to add that hasn't been mentioned.
    - React to the original comment with a thumbs up.
    - Please do not add comments like "+1" or "I'm also having this issue". It
is more beneficial to keep responses on-topic and concise.
- Ensure the enhancement hasn't already been added to the latest version.

### Submitting a Good Enhancement
Enhancements, like buts, are tracked using GitHub's built-in 
[issues](https://github.com/bastisawesome/spkg/issues) page. When submitting an
enhancement, please do the following:
- Include a short and concise title detailing the enhancement.
- In the body, provide more detailed explanations of the enhancement.
- Describe how the enhancement differs from the existing behaviour and how it
would benefit the community to change or add this enhancement.
- Include information about the operating system you are using:
    - OS name
    - OS version
    - Python version

Enhancement reports should contain only a single enhancement, if you have
multiple suggestions, open one issue for each enhancement. If they are related
in some way, be sure to reference them in the descriptions.

## Issue/Enhancement Labels
This section describes the labels used to organise and track issues and
enhancements.

| Label name  | Search | Description |
| --- | --- | --- |
| `enhancement` | [search](https://github.com/bastisawesome/spkg/labels/enhancement) | Feature requests. |
| `bug` | [search](https://github.com/bastisawesome/spkg/labels/bug) | Possible or confirmed bugs. |
| `documentation` | [search](https://github.com/bastisawesome/spkg/labels/documentation) | Enhancements to the documentation and help output. |
| `duplicate` | [search](https://github.com/bastisawesome/spkg/labels/duplicate) | Issues that have already been reported. |
| `good first issue` | [search](https://github.com/bastisawesome/spkg/labels/good%20first%20issue) | Issues that can either be solved in very little code, or would be good for getting accustomed to the codebase. |
| `help wanted` | [search](https://github.com/bastisawesome/spkg/labels/help%20wanted) | Issues that are more complex and may require better knowledge and understanding of the underlying code infrastructure. |
| `invalid` | [search](https://github.com/bastisawesome/spkg/labels/invalid) | Issues that aren't related to SPKG. |
| `wontfix` | [search](https://github.com/bastisawesome/spkg/labels/wontfix) | Issues that will not be fixed, usually due to working as intended or outside of scope. |

## Code Contributions
If you're not sure where to begin with contributing, look for issues labelled as
"help wanted" or "good first issue".
- [Help wanted issues](https://github.com/bastisawesome/spkg/labels/help%20wanted) -
Usually a little more complex and may require a bit of
code refactoring or knowledge on underlying requirements (like with Requests).
- [Good first issue](https://github.com/bastisawesome/spkg/labels/good%20first%20issue) -
Usually simpler to implement with very little refactoring or knowledge of
underlying requirements.

## Pull Requests
All contributions must be made through pull requests into the dev branch. Pull
requests targetted at any other branches will be immediately disregarded. This
is to ensure the code works correctly and is compatible with other changes being
made.

Pull requests must use the following guidelines to be considered:
- Must follow the [styleguide](#styleguide)
- Must include in the body what issue(s) or enhancement(s) it resolves:
    - `closes #[issue number]`

## Styleguide
### Git Commit Messages
- Use the present tense ("Fix bug" not "Fixed bug")
- Use the imperative mood ("Fix bug" not "Fixes bug")
- Limit the first line to 80 characters or less
- Reference **all** issues and pull requests resolved

### Python Styleguide
SPKG is linted with the following:
- Pylint
- Flake8
- Pylance

If using VSCode, Pylance is required to be used, and one of either Pylint or
Flake8 must also be used.

If contributions are made in another editor, make sure to mention it in the
description of the pull request, as code will have to be checked against
PyLance.

SPKG abides by [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards,
with the following modifications:
- Lines must be 80 characters long or less
- Indentation is 4-spaces

The following options are used:
Flake8:
- --max-line-len=80

Pylint:
- --disable=missing-module-docstring,missing-function-docstring,invalid-name,missing-class-docstring,redefined-outer-name

- Avoid unnecessary global variables.
- Python standard library imports are first, then external modules, and finally
local files.
- Variables should use type declarations unless they are declared with the
result of a type-declared function.

Supported Python versions:
- Python 3.8+

Pylint and/or Flake8 will both catch most style problems, and SPKG has been
tested with both enabled. **Do not disable any linter options in code provided
in pull requests.**
