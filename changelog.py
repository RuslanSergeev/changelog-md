#!python3

import sys
import re
import argparse
import subprocess as sp
from collections import defaultdict

def redirect_output(filename):
    try:
        sys.stdout = open(filename, 'w')
    except Exception as e:
        print('unable to open: ', e.args)

def prepare_log():
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

def parse_comment(changelog, tag, comment):
    tokens=['[feature]', '[fix]', '[changelog]']
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


def parse_git_log(log_out):
    #until first valid tag in timeline
    #everything is unreleased
    tag='unreleased'
    changelog=defaultdict(lambda: defaultdict(list))
    for log in log_out:
        comment = log[0]
        reflog = log[1]
        date = log[2]
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
        parse_comment(changelog, tag, comment)
    return changelog

def print_section(d, key, section_text):
    if len(d[key]):
        print(section_text)
        for feat in d[key]:
            print(f' - [x] {feat}')

def print_summary(d):
    summary = list(filter(lambda line: len(line), d['summary']))
    if len(summary):
        print("```")
        for sumline in d['summary']:
            if len(sumline):
                print(sumline)
        print("```")

def print_changelog(changelog):
    for k, v in changelog.items():
        print('\n---\n')
        print(f'# {k} ({v["date"]} )\n')
        print_summary(v)
        print_section(v, '[feature]', '### new features:')
        print_section(v, '[fix]', '### bug fixes:')
        print_section(v, '[changelog]', '### minor changes:')


if __name__ == '__main__':
    description = '''
    This script will make changelog,
    for git tracked projects
    '''
    epilog='''
    \x1b[36m
    commit message format:
    [feature]|[fix]|[changelog] actual_commit_message
    [feature] stands for new major features introduced by the commit
    [fix] for major buxfixes made by commit
    [changelog] else additional helpfull information for changelog
    \x1b[0m'''
    parser = argparse.ArgumentParser(description=description,
        epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--logname', default='changelog.md',
        help='filename for the changelog')
    args=parser.parse_args()
    redirect_output(args.logname)
    log = prepare_log()
    changelog = parse_git_log(log)
    print_changelog(changelog)
