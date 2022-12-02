# sedmv2
Respository for SEDMv2 scheduling, observations, and data reduction

## get_observation
Called from ROS (robo control software). Queries the schedule from Fritz for SEDMv2, schedule returns unexpired requests with 'submitted' string in status ordered by priority and observability. Selects the top request and saves it to queue_target.dat in /home/sedm/Queue/sedmv2 folder which is read by ROS. Returns 0 is successful, and other error codes if not (see below).

1: could not access queue (either token not found or error in schedule query)
2: no observations to schedule
5: Some required column missing from selected request
6: Error in saving queue_target.dat

## observation_status
Called from ROS. Takes a request_id and a status int (0:completed, 1:failed, 2:skipped). Queries the request_id to get allocation_id and object_id and updates the status of the request. Returns 0 if successful, 1 if there was an error.

## reset_skipped
To run at the end of every night (either from ROS or independently). Queries all requests with status=skipped. Resets their status to 'submitted'.
