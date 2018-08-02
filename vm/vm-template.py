"""

Create one or more VMs

"""

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1'


def GenerateConfig(context):
  """
  Generates config
  """

  project_id = context.env['project']

  config = {'resources': []}
  num    = 1

  try:
    count = context.properties['vmCount']
  except KeyError:
    count = 1

  try:
    tags = context.properties['tags']
  except KeyError:
    tags = []

  for i in range(int(count)):

    vm = {
      'name': 'vm-' + context.env['name'] + '-' + str(num),
      'type': 'compute.v1.instance',
      'properties': {
          'zone': context.properties['zone'],
          'machineType': ''.join(
            [
              COMPUTE_URL_BASE,
              '/projects/', project_id,
              '/zones/', context.properties['zone'],
              '/machineTypes/', context.properties['machineType']
            ]
          ),
          'tags': {
              'items': tags,
          },
          'disks': [{
              'deviceName': 'boot',
              'type': 'PERSISTENT',
              'boot': True,
              'autoDelete': True,
              'initializeParams': {
                  'sourceImage': ''.join(
                    [
                      COMPUTE_URL_BASE, '/', context.properties['sourceImage']
                    ]
                  ),
              }
          }],
          'networkInterfaces': [{
              'network': ''.join(
                [
                  COMPUTE_URL_BASE,
                  '/projects/', project_id,
                  '/global/networks/', context.properties['network']
                ]
              ),
              'subnetwork': ''.join(
                [
                  COMPUTE_URL_BASE,
                  '/projects/', project_id,
                  '/regions/', context.properties['region'],
                  '/subnetworks/', context.properties['subnetwork']
                ]
              ),
              'accessConfigs': [{
                  'name': 'External NAT',
                  'type': 'ONE_TO_ONE_NAT'
              }]
          }]
      }
    }

    config['resources'].append(vm)
    num += 1

  return config

