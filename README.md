# request-batcher

Note, `sh fire_requests.sh` will fire a large number of requests concurrently. This doesn't work very well locally, it actually runs out of ports...

The idea here is purely state-driven. If you rely on this data to persist 
then don't use this, or adapt it and add rabbitmq plus another service 
consuming from there!  The use-case here is for a system which wants to respond
to email open and clicks within 10 seconds of the event occurring.

The idea is to accept a large number of requests on a server designed to deal with it, 
store data in memory, then package the data received
into a single request, suited more to a server not running an event loop (e.g. Django).

I'll update this README soon
