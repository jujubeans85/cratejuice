exports.handler = async function(event, context) {
  const payload = {
    ok: true,
    source: 'netlify-function',
    path: event.path,
    method: event.httpMethod || event.http_method || null,
    query: event.queryStringParameters || event.query || null
  };

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  };
};
