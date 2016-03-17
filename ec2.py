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

sub_parser = sub_parsers.add_parser('ids')
sub_parser.set_defaults(target='ids')
sub_parser.set_defaults(func=ids)
sub_parser.add_argument('--name')

def names(ns):
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        name = ''
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                name = tag['Value']
                break
        print(name)

sub_parser = sub_parsers.add_parser('names')
sub_parser.set_defaults(target='names')
sub_parser.set_defaults(func=names)

def status(ns):
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        name = getInstanceName(instance)
        print("id : {0}, {2} ({1})".format(
            instance.instance_id,
            name,
            instance.state['Name']
            ))

sub_parser = sub_parsers.add_parser('status')
sub_parser.set_defaults(target='status')
sub_parser.set_defaults(func=status)

def ip_pub(ns):
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        printIfMatchOrEmpty(getInstanceName(instance), ns.name, instance.public_ip_address)

sub_parser = sub_parsers.add_parser('ip_pub')
sub_parser.set_defaults(target='ip_pub')
sub_parser.add_argument('--name')
sub_parser.set_defaults(func=ip_pub)

def start(ns):
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        if ns.name and getInstanceName(instance) in ns.args:
            instance.start()
        elif instance.id in ns.args:
            instance.start()

sub_parser = sub_parsers.add_parser('start')
sub_parser.set_defaults(target='start')
sub_parser.add_argument('--name', action='store_true')
sub_parser.add_argument('args')
sub_parser.set_defaults(func=start)

def stop(ns):
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        if ns.name and getInstanceName(instance) in ns.args:
            instance.stop()
        elif instance.id in ns.args:
            instance.stop()

sub_parser = sub_parsers.add_parser('stop')
sub_parser.set_defaults(target='stop')
sub_parser.add_argument('--name', action='store_true')
sub_parser.add_argument('args')
sub_parser.set_defaults(func=stop)

# --------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------
def main():
    namespace = parser.parse_args()

    if namespace.target is not None:
        namespace.func(namespace)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

