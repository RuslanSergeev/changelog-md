from .logger import logger
import argparse

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
[internal] messages used only for internal changelogs. These messages can be
    ommited for your customers with flag '--internal yes'.
\x1b[0m'''
parser = argparse.ArgumentParser(description=description,
    epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--logname', default='changelog.md', type=str,
    help='Filename for the changelog')
parser.add_argument('--internal', default=False, type=bool,
    help='If internal is False, [internal] commit messages are ommited.')
parser.add_argument('release',  type=str,
    help='Tagname for the unreleased commits.')
parser.add_argument('annotation', type=str,
    help='Annotation for the release. Must contain summary information.')
args=parser.parse_args()

l = logger(args.release, args.annotation, args.logname, args.internal)
l.make()