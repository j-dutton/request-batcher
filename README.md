# request-batcher

Note, `sh fire_requests.sh` will fire a large number of requests concurrently. This doesn't work very well locally, it actually runs out of ports...

The idea here is purely state-driven. If you rely on this data, don't use this. The idea is to accept a large number
of requests on a server designed to deal with it, store data in state, then package the data received
into a single request, suited more to a server not running an event loop.
