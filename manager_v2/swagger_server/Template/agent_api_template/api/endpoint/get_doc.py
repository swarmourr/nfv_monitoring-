from api.restplus import api



def get_ctx():
  app.app_context().__enter__()
  ff = open('schema.json', 'wb')
  ff.write(json.dumps(api.__schema__))
  ff.close()
  conv('schema.json')
  return api.__schema
