# Readme on changelog.py

### execution information:
This script aim to provide changelogs on git-tracked projects.
Run `changelog.py` script in your directory 
and it'll generate the changelog file.
In order to obtain actual changelog, run:

```shell
python3 changelog.py vX.Y.Z "Annotation for this version"
git commit --amend
git push
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
[internal] this section will be generated only if --internal argument is given.
This commit message string will be ommited from changelog.
```

### Releases:
Any tagged commit will be interpreted as release.
To create tag, write:
```
git tag -a v<version>
... tag anotation ...
git push --follow-tags
```
Any commit above the last tag will be marked as tag provided 
in command line arguments and annotated accordingly.
