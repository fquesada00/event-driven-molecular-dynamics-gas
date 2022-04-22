from file_read_backwards import FileReadBackwards
from collections import deque

# @link = https://pypi.org/project/file-read-backwards/
def get_equilibrium_iterations(file_path, equilibrium_time):
    equilibrium_iterations_data = deque([])
    last_event_time = -1
    with FileReadBackwards(file_path, encoding="utf-8") as simulation_file:
        # Initialize
        iteration_data = deque([])
        for line in simulation_file:
            line_data = line.split()
            if len(line_data) == 1:
                iteration_time = float(line_data[0])
                # If no last event time set, then do it
                if last_event_time == -1:
                    last_event_time = iteration_time
                elif (last_event_time - iteration_time) >= equilibrium_time:
                    # If the last event time is set, then check if the iteration time is
                    # in the equilibrium time range, if not, then stop
                    break

                # Add to the iteration data
                equilibrium_iterations_data.appendleft(list(iteration_data))

                # Add time to the iteration data
                iteration_data.appendleft(iteration_time)

                # Prepare for next iteration
                iteration_data = deque([])
            else:
                # Format: x y vx vy <'x' | 'y' | 'p' | '-'>
                iteration_data.appendleft(line_data)
    
    # Return the equilibrium iterations data
    return list(equilibrium_iterations_data)
                    