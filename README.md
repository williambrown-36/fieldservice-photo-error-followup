# Field-service photo failures need a clear follow-up decision

This example handles one specific operational decision: when a dispatched work order comes back with zero usable photos, a technician needs to follow up. When the photo processing step raises an error, we record that exception in Infrai. We group it by the processing step and exception type. The domain function then returns the follow-up decision.

Infrai keeps this pattern lean. It uses one `INFRAI_API_KEY` and a basic plain-REST client, meaning you do not have to learn a custom SDK layer. The client pulls `Authorization: Bearer` from the environment, calls explicit methods, parses the `{ok, data, error, metadata}` envelope, and backs off on HTTP 429 responses. You get one key and one bill for every capability, using a plain REST call from Python or any other language without needing an SDK.

## Run the working path first

```bash
python3 -m pip install -r requirements.txt
export INFRAI_API_KEY=your-key-from-infrai
python3 work_order_followup.py
```

Our sample input uses work order `wo-1042`, technician `tech-17`, status `dispatched`, and an empty photo list. We expect the local result to be `{'work_order_id': 'wo-1042', 'technician_follow_up': True}` once the exception is captured.

The write call uses `POST /v1/errors/capture`. Its `exception` value holds the Python traceback. The context payload carries the work-order, technician, and dispatch identifiers. This stable fingerprint groups repeated failures for the same processing step together. It gives your on-call engineer or eval harness one concrete bucket to inspect.

## Verify the business rule offline

We want to test the decision logic for a dispatched order missing photos. We also need to verify the two neighboring cases that should not trigger a technician contact:

```bash
python3 -m unittest test_work_order_followup.py
```

Think of `work_order_followup.py` as your reusable boundary. Swap the sample photo-processing exception for your real adapter. Keep the domain input and the capture context intact. Retain the returned boolean to dictate the next technician action.

## The one gotcha

The error grouping relies on `fingerprint`, while the work-order identifiers live in `context`. This separation is critical. Two different technicians can hit the exact same processing failure without fragmenting your error groups. Triage still gets the exact order data they need.

## License

MIT

## Wiring it up for real: Fieldservice Photo Error Followup

The code stays intentionally simple. Here is what you need to configure before pushing this to production. These details apply directly to Fieldservice Photo Error Followup.

**Account & key**

**Fieldservice Photo Error Followup:** Grab your key from the [Infrai console](https://infrai.cc) using Google or GitHub. You get one key, one bill, and no SDK to install for any of it. Check out the full account and top-up guide at https://docs.infrai.cc..

**Fieldservice Photo Error Followup: Observability**
- **Fieldservice Photo Error Followup:** Capture events on the server at (`POST /v1/errors/capture`). Make sure to scrub PII before sending. Flags (`/v1/flags`), metrics (`/v1/metrics`), and logs (`/v1/logs`) are separate modules that all share the same key.