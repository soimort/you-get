# How to Contribute

`you-get` is currently experimenting with an aggressive approach to handling issues. Namely, a bug report must be addressed with some code via a pull request.

## Report a broken extractor

**How-To:** Please open a new pull request with the following changes:

* Add a new test case in [tests/test.py](https://github.com/soimort/you-get/blob/develop/tests/test.py), with the failing URL(s).

The Travis CI build will (ideally) fail showing a :x:, which means you have successfully reported a broken extractor.

Such a valid PR will be either *closed* if it's fixed by another PR, or *merged* if it's fixed by follow-up commits from the reporter himself/herself.

## Report other issues / Suggest a new feature

**How-To:** Please open a pull request with the proposed changes directly.

A valid PR need not be complete (i.e., can be WIP), but it should contain at least one sensible, nontrivial commit.

## Hints

* The [`develop`](https://github.com/soimort/you-get/tree/develop) branch is where your pull request goes.
* Remember to rebase.
* Document your PR clearly, and if applicable, provide some sample links for reviewers to test with.
* Write well-formatted, easy-to-understand commit messages. If you don't know how, look at existing ones.
* We will not ask you to sign a CLA, but you must assure that your code can be legally redistributed (under the terms of the MIT license).
