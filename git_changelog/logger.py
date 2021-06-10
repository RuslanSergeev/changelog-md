#!python3

import sys
import re
import argparse
import subprocess as sp
from datetime import datetime
from collections import defaultdict

class logger:
    def __init__(self, release, annotation, logname='changelog.md', internal=False):
        self.release = release
        self.annotation = annotation
        self.logname = logname
        self.internal = internal

    def make(self):
        self.__redirect_output(self.logname)
        log = self.__prepare_log()
        changelog = self.__parse_git_log(log, self.release, self.annotation)
        self.__print_changelog(changelog, self.internal)

    def __redirect_output(self, filename):
        try:
            sys.stdout = open(filename, 'w')
        except Exception as e:
            print('unable to open: ', e.args)

    def __prepare_log(self, ):
        log_proc = sp.run('git log --date=format:\'%Y.%m.%d\' --pretty=format:\'%s | %D | %ad\'',
            shell=True, stdout=sp.PIPE, universal_newlines=True);
        code=log_proc.returncode
        if code:
            print(f'git returned error code: {code}')
            exit(code)
        #list of lines
        log=log_proc.stdout.split('\n')
        #list of lists of fields
        #[[comment, relog, date]]
        log=list(map(lambda line: line.split('|'), log))
        return log

    def __parse_comment(self, changelog, tag, comment):
        tokens=['[feature]', '[fix]', '[changelog]', '[internal]']
        comment = comment.split(' ')
        comment = list(filter(lambda word: len(word), comment))
        token='[else]' #everything else falls in [else] section.
        description = ''
        for word in comment:
            if word in tokens:
                if len(description):
                    changelog[tag][token].append(description)
                token = word
                description = ''
            else:
                description = description +' '+word
        if len(description):
            changelog[tag][token].append(description)


    def __parse_git_log(self, log_out, tagname='unreleased', summary='no summary'):
        #until first valid tag in timeline
        #everything is unreleased
        changelog=defaultdict(lambda: defaultdict(list))
        tag=tagname
        changelog[tag]['summary'] = summary.split('\n')
        changelog[tag]['date'] = datetime.now().strftime('%Y.%m.%d')
        for log in log_out:
            comment, reflog, date = log
            tagmatch = re.search(r'(?<=tag: )([\w.]+)', reflog)
            if tagmatch:
                #there is new release tag.
                tag=tagmatch.group(0)
                #add tag annotation for release
                tag_proc = sp.run(f'git for-each-ref refs/tags/{tag} --format=\'%(contents)\'',
                    shell=True, stdout=sp.PIPE, universal_newlines=True);
                tagsum=tag_proc.stdout.split('\n')
                changelog[tag]['summary'] = tagsum
                changelog[tag]['date'] = date
            self.__parse_comment(changelog, tag, comment)
        return changelog

    def __print_section(self, d, key, section_text):
        if len(d[key]):
            print(section_text)
            for feat in d[key]:
                print(f' - [x] {feat}')

    def __print_summary(self, d):
        summary = list(filter(lambda line: len(line), d['summary']))
        if len(summary):
            print("```")
            for sumline in d['summary']:
                if len(sumline):
                    print(sumline)
            print("```")

    def __print_changelog(self, changelog, is_internal=False):
        for k, v in changelog.items():
            print('\n---\n')
            print(f'# {k} ({v["date"]} )\n')
            self.__print_summary(v)
            self.__print_section(v, '[feature]', '### new features:')
            self.__print_section(v, '[fix]', '### bug fixes:')
            self.__print_section(v, '[changelog]', '### minor changes:')
            if is_internal:
                self.__print_section(v, '[internal]', '### for developers only:')

                