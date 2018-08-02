"""

Create one or more VMs

"""

COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1'


def GenerateConfig(context):
  """
  Generates config
  """

  config = {'resources': []}
  num    = 1

  try:
    tags = context.properties['tags']
  except KeyError:
    tags = []

  project_id = context.env['project']
  zones      = context.properties['zones']

  for zone in zones:

    region = zone.split('-')[0] + '-' + zone.split('-')[1]

    vm = {
      'name': 'vm-' + context.env['name'] + '-' + str(num),
      'type': 'compute.v1.instance',
      'properties': {
          'zone': zone,
          'machineType': ''.join(
            [
              COMPUTE_URL_BASE,
              '/projects/', project_id,
              '/zones/', zone,
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
                  '/regions/', region,
                  '/subnetworks/', context.properties['network'], '-sub1-', region
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

