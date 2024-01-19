#!/usr/bin/python3

import sys, os, json
from kubernetes import client, config

# choosen namespace
namespace = os.getenv('namespace')

# kubernetes config
config.load_kube_config()

# get namespaces
api = client.CoreV1Api()
pods = api.list_namespaced_pod(namespace)

# create output list
items = []
pod_status_index = 0

for pod in pods.items:
  tempdict = {}
  tempdict['title'] = pod.metadata.name
  tempdict['arg'] = pod.metadata.name
  tempdict['icon'] = {'path':'./resources/pod.png'}

  for i,cond in enumerate(pod.status.conditions):
    if cond.type == 'Ready':
      pod_status_index = i

  tempdict['subtitle'] = 'Ready: {}'.format(pod.status.conditions[pod_status_index].status)
  items.append(tempdict)

if len(items) == 0:
  tempdict = {}
  tempdict['title'] = 'No pods in {}'.format(namespace)
  tempdict['arg'] = 'none'
  items.append(tempdict)

jsondict = {}
jsondict['items'] = items
jsonstr = json.dumps(jsondict)

# pass output to Alfred
sys.stdout.write(jsonstr)