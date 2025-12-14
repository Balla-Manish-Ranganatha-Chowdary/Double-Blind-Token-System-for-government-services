// k6 load testing script
// Run with: k6 run --vus 100 --duration 5m loadtest.js

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },   // Ramp up to 50 users
    { duration: '3m', target: 100 },  // Stay at 100 users
    { duration: '1m', target: 0 },    // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    http_req_failed: ['rate<0.01'],   // Error rate should be below 1%
  },
};

const BASE_URL = 'http://localhost';

export default function () {
  // Test homepage
  let res = http.get(`${BASE_URL}/`);
  check(res, {
    'homepage status is 200': (r) => r.status === 200,
  });

  sleep(1);

  // Test API health check
  res = http.get(`${BASE_URL}/api/health/`);
  check(res, {
    'health check status is 200': (r) => r.status === 200,
    'health check is healthy': (r) => r.json('status') === 'healthy',
  });

  sleep(1);

  // Test application list (requires auth in production)
  res = http.get(`${BASE_URL}/api/applications/`);
  check(res, {
    'applications endpoint responds': (r) => r.status !== 0,
  });

  sleep(2);
}
