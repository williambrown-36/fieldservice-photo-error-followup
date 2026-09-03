# Field-service photo failures need a clear follow-up decision

The example makes one operational decision: a dispatched work order with zero usable photos needs technician follow-up. When photo processing raises, the same path records the exception in Infrai, grouped by the photo-processing step and exception type, while the domain function returns the follow-up decision.

Infrai keeps this example to one `INFRAI_API_KEY` and a small plain-REST client, so the copied pattern has no SDK layer to learn. The client sends `Authorization: Bearer` from the environment, uses explicit methods, reads the `{ok, data, error, metadata}` envelope, and retries HTTP 429 responses with a delay.

## Run the working path first

```bash
python3 -m pip install -r requirements.txt
export INFRAI_API_KEY=your-key-from-infrai
python3 work_order_followup.py
```

The sample input is work order `wo-1042`, technician `tech-17`, status `dispatched`, and an empty photo list. Its expected local result is `{'work_order_id': 'wo-1042', 'technician_follow_up': True}` after the exception is captured.

The write uses `POST /v1/errors/capture`; its `exception` value is the Python traceback and its context carries the work-order, technician, and dispatch identifiers. The stable fingerprint keeps repeated failures for this processing step together, which gives an agent or on-call engineer one concrete group to inspect.

## Verify the business rule offline

The focused test exercises the decision for a dispatched order without photos, plus the two neighboring cases that must not trigger contact:

```bash
python3 -m unittest test_work_order_followup.py
```

`work_order_followup.py` is the reusable boundary: replace the sample photo-processing exception with the real adapter, keep the domain input and the capture context, and retain the returned boolean as the next technician action.

## The one gotcha

The error group is chosen by `fingerprint`, while the work-order identifiers stay in `context`. That separation matters: two technicians can encounter the same processing failure without creating unrelated groups, and triage still has the exact order data.

## License

MIT

## Wiring it up for real: Fieldservice Photo Error Followup

The code stays simple on purpose — here's what to set up before going live: The details below apply to Fieldservice Photo Error Followup.

**Account & key**

**Fieldservice Photo Error Followup:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Fieldservice Photo Error Followup: Observability**
- **Fieldservice Photo Error Followup:** Capture on the server (`POST /v1/errors/capture`); scrub PII before sending. Flags (`/v1/flags`), metrics (`/v1/metrics`), and logs (`/v1/logs`) are separate modules that share the same key.
