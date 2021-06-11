# install with pip
```bash
python3 -m pip install changelog-md
``` 

# install with Poetry
```
poetry add changelog-md
```

# execution information:

This script aim to provide changelogs on git-tracked projects.
Run `changelog.py` script in your directory 
and it'll generate the changelog file.
In order to obtain actual changelog, run:


You can use git changelog from command line directly:
```bash
# ... code on project
git commit                                                    #add your commit message on work you've done
python3 -m changelog-md vX.Y.Z "Annotation for this version" #generate changelog
git add changelog.md                                          #stage the changelog to current commit
git commit --amend                                            #add the changelog to current commit, leave commit message as is.
git tag -a vX.Y.Z -m "Annotation for this version"            #add the tag you've set earlier in changelog.
git push --follow-tags                                        #publish your changes and the new tag.
```

Or you can elaborate your workflow python scripts 
to use changelog-md as a python module:
```python
# CICD_script.py
# ... do some CICD work

from changelog-md import logger
l = logger('vX.Y.Z', 'Annotation for this version')           #create logger instance
l.make()                                                      #print the log

# ... do other CICD work
```


More actual information on colophon of scripts:
```shell
#actual information on colophon:
python3 -m changelog-md --help
```

# correct commit messages:

To make this scripts work properly, your commit messages
should look like any of this:
```
[feature] feature description here
[fix] fix description
[changelog] minor changes description
[internal] this section will be generated only if --internal argument is given.
This commit message string will be ommited from changelog.
```

#  Releases:

Any tagged commit will be interpreted as release.
To create tag, write:
```
git tag -a v<version>
... tag anotation ...
git push --follow-tags
```
Any commit above the last tag will be marked as tag provided 
in command line arguments and annotated accordingly.
