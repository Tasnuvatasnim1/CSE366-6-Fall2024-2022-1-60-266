# Class Schedule Optimization

This project optimizes class schedules using a genetic algorithm. It assigns classes to students based on their preferences and availability while aiming to maximize the overall fitness of the schedule.

## Prerequisites

1. Python 3.8 or higher
2. Required libraries:
   - `pygame`
   - `numpy`

You can install the required libraries by running:
```bash
pip install pygame numpy
```

## Project Structure

- **`environment.py`**: Defines the environment and the classes available.
- **`run.py`**: Main script to run the scheduler.
- **`fitness_trends.log`**: Logs the best fitness score for each generation.

## Running the Code

1. Clone the repository or download the source files.
2. Open a terminal in the project directory.
3. Run the following command:
   ```bash
   python run.py
   ```
4. A window will appear showing the current generation's best schedule and fitness score.
5. The program runs for a maximum of 100 generations. Close the window to stop the execution early.

## Output

- **Visual Output**:
  - A grid showing the current generation's best schedule.
  - Stats including generation number and best fitness score for the generation.

- **Log File**:
  - The `fitness_trends.log` file will contain the best fitness score for each generation.

## Customization

- **Mutation Rate**:
  - Adjust the mutation rate in the `mutate` function in `run.py`.

- **Number of Generations**:
  - Modify the `generation_count` loop condition in `run_scheduler()`.

- **Number of Classes**:
  - Update `num_classes` in `run_scheduler()`.

## Stopping the Program

- Close the visualization window by clicking the close button.
- Alternatively, use `Ctrl+C` in the terminal.

## Notes

- Ensure your screen resolution is sufficient to display the visualization (minimum 1200x800).
- If using an IDE, make sure the `pygame` window is in focus to avoid input lag.

