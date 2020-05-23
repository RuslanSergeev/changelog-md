# Readme on changelog.py

### execution information:
This script aim to provide changelogs on git-tracked projects.
place any of this scripts (changelog.py or changelog.sh) in your repo.
When you want to obtain actual changelog, run:

```shell
python3 changelog.py #any system with Python3
./changelog.sh #for systems with bash
```

More actual information on colophon of scripts:
```shell
#actual information on colophon:
python3 changelog.py --help
```

### correct commit messages:
To make this scripts work properly, your commit messages
should look like any of this:
```
[feature] feature description here
[fix] fix description
[changelog] minor changes description
```

### Releases:
Any tagged commit will be interpreted as release.
To create tag, write:
```
git tag -a v<version>
... tag anotation ...
git push --follow-tags
```
Any commit above the last tag, will fall in **Unreleased** section.
