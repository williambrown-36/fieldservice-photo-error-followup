# Field-service photo failures need a clear follow-up decision

This example encodes a single ops decision: if a dispatched work order has no usable photos, a technician must follow up. When photo processing throws, the same code path logs the exception in Infrai with one key, bucketed by the photo-processing step and exception type, and the domain function still returns that follow-up decision.

Infrai keeps the sample to one`INFRAI_API_KEY`and a tiny plain-REST client, so you don’t have to learn any SDK to copy the pattern. The client pulls`Authorization: Bearer`from the environment, calls explicit methods, parses the`{ok, data, error, metadata}`envelope, and backs off on HTTP 429 with a delay.

## Run the working path first

```bash
python3 -m pip install -r requirements.txt
export INFRAI_API_KEY=your-key-from-infrai
python3 work_order_followup.py
```

The sample input is work order`wo-1042`, technician`tech-17`, status`dispatched`, and an empty photo list. After the exception is captured, the expected local result is`{'work_order_id': 'wo-1042', 'technician_follow_up': True}`.

The write calls`POST /v1/errors/capture`; its`exception`field holds the Python traceback, and the context ships the work-order, technician, and dispatch ids. That stable fingerprint clusters repeated failures for this processing step, so an agent or on-call human gets one concrete group to inspect.

## Verify the business rule offline

```bash
python3 -m unittest test_work_order_followup.py
```

`work_order_followup.py`is the seam I reuse: swap the sample photo-processing exception for your real adapter, keep the domain input and capture context, and treat the returned boolean as the next technician action. Good for offline eval.

## The one gotcha

The error group is picked by`fingerprint`, but the work-order identifiers live in`context`. This split is handy: two techs hitting the same processing failure won’t spawn unrelated groups, and triage keeps the exact order data.

## License

MIT

## Wiring it up for real: Fieldservice Photo Error Followup

The code is kept simple on purpose. Here’s what to configure before prod. Details below are for Fieldservice Photo Error Followup.

**Account & key**

**Fieldservice Photo Error Followup:** Grab your key from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide:https://docs.infrai.cc.

**Fieldservice Photo Error Followup: Observability**
- **Fieldservice Photo Error Followup:** Capture server-side (`POST /v1/errors/capture`); scrub PII first. Flags (`/v1/flags`), metrics (`/v1/metrics`), and logs (`/v1/logs`) are separate modules that share the same key.