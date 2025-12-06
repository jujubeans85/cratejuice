exports.handler = async function(event, context) {
  let parsedBody = null;
  try {
    parsedBody = event.body ? JSON.parse(event.body) : null;
  } catch (e) {
    parsedBody = event.body || null;
  }

  const payload = {
    ok: true,
    source: 'netlify-function-echo',
    path: event.path,
    method: event.httpMethod || event.http_method || null,
    query: event.queryStringParameters || event.query || null,
    body: parsedBody
  };

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  };
};
