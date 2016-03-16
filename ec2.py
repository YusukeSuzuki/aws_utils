#!/usr/bin/env python3
import sys
import argparse
import boto3

# --------------------------------------------------------------------------------
# other functions 
# --------------------------------------------------------------------------------

def getInstanceName(instance):
    for tag in instance.tags:
        if tag['Key'] == 'Name':
            return tag['Value']
    return ''

def printIfMatchOrEmpty(ins, cond, out):
    if cond == '' or ins == cond:
        print(out)

# --------------------------------------------------------------------------------
# sub commands
# --------------------------------------------------------------------------------
def ids(ns):
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        printIfMatchOrEmpty(getInstanceName(instance), ns.name, instance.instance_id)

def names(ns):
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        name = ''
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                name = tag['Value']
                break
        print(name)

def status(ns):
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        name = getInstanceName(instance)
        print("id : {0}, {2} ({1})".format(
            instance.instance_id,
            name,
            instance.state['Name']
            ))

# --------------------------------------------------------------------------------
# arg parse
# --------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='ec2 utils')
parser.set_defaults(target='')

sub_parsers =  parser.add_subparsers(title='subcommands')

parser_names = sub_parsers.add_parser('names')
parser_names.set_defaults(target='names')

parser_ids = sub_parsers.add_parser('ids')
parser_ids.set_defaults(target='ids')
parser_ids.add_argument('--name')

parser_status = sub_parsers.add_parser('status')
parser_status.set_defaults(target='status')

# --------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------
def main():
    namespace = parser.parse_args()
    
    if namespace.target == 'names':
        names(namespace)
    elif namespace.target == 'ids':
        ids(namespace)
    elif namespace.target == 'status':
        status(namespace)

if __name__ == '__main__':
    main()

