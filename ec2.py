#!/usr/bin/env python3
import sys
import argparse
import boto3

# --------------------------------------------------------------------------------
# arg parse
# --------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='ec2 utils')
parser.set_defaults(target='')

sub_parsers =  parser.add_subparsers(title='sub commands')

# --------------------------------------------------------------------------------
# other functions 
# --------------------------------------------------------------------------------

def getInstanceName(instance):
    for tag in instance.tags:
        if tag['Key'] == 'Name':
            return tag['Value']
    return None

def printIfMatchOrEmpty(ins, cond, out):
    if cond == None or ins == cond:
        print(out)

# --------------------------------------------------------------------------------
# sub commands
# --------------------------------------------------------------------------------
def ids(ns):
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        printIfMatchOrEmpty(getInstanceName(instance), ns.name, instance.instance_id)

parser_ids = sub_parsers.add_parser('ids')
parser_ids.set_defaults(target='ids')
parser_ids.add_argument('--name')

def names(ns):
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        name = ''
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                name = tag['Value']
                break
        print(name)

parser_names = sub_parsers.add_parser('names')
parser_names.set_defaults(target='names')

def status(ns):
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        name = getInstanceName(instance)
        print("id : {0}, {2} ({1})".format(
            instance.instance_id,
            name,
            instance.state['Name']
            ))

parser_status = sub_parsers.add_parser('status')
parser_status.set_defaults(target='status')

def ip_pub(ns):
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        printIfMatchOrEmpty(getInstanceName(instance), ns.name, instance.public_ip_address)

parser_ids = sub_parsers.add_parser('ip_pub')
parser_ids.set_defaults(target='ip_pub')
parser_ids.add_argument('--name')

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
    elif namespace.target == 'ip_pub':
        ip_pub(namespace)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

