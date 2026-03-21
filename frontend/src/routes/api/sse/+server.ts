import type { RequestHandler } from './$types';

const BACKEND_STREAM_URL = 'http://localhost:8000/stream';

export const GET: RequestHandler = async ({ url }) => {
  const keyword = url.searchParams.get('keyword');

  if (!keyword || keyword.trim() === '') {
    return new Response('data: {"status":"error","message":"keyword is required"}\n\n', {
      status: 400,
      headers: { 'Content-Type': 'text/event-stream' },
    });
  }

  let response: Response;
  try {
    response = await fetch(
      `${BACKEND_STREAM_URL}?keyword=${encodeURIComponent(keyword)}`,
    );
  } catch {
    return new Response(
      'event: error\ndata: {"status":"error","message":"Backend unreachable"}\n\n',
      {
        status: 502,
        headers: { 'Content-Type': 'text/event-stream' },
      },
    );
  }

  if (!response.ok || !response.body) {
    return new Response(
      'event: error\ndata: {"status":"error","message":"Backend error"}\n\n',
      {
        status: 502,
        headers: { 'Content-Type': 'text/event-stream' },
      },
    );
  }

  const upstream = response.body;

  const stream = new ReadableStream({
    start(controller) {
      const reader = upstream.getReader();

      function push() {
        reader
          .read()
          .then(({ done, value }) => {
            if (done) {
              controller.close();
              return;
            }
            controller.enqueue(value);
            push();
          })
          .catch((err: unknown) => {
            controller.error(err);
          });
      }

      push();
    },
    cancel() {
      upstream.cancel();
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no',
    },
  });
};
