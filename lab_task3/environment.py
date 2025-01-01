# environment.py
import pygame
import numpy as np
from agent import Student

class Environment:
    def __init__(self, num_classes, num_students=5, num_time_slots=8):
        self.num_classes = num_classes
        self.num_students = num_students
        self.num_time_slots = num_time_slots
        
        # Initialize classes with priorities (1-5) and durations (1-2 hours)
        self.classes = []
        for i in range(num_classes):
            priority = np.random.randint(1, 6)  # Priority from 1 to 5
            duration = np.random.randint(1, 3)  # Duration 1 or 2 hours
            self.classes.append({
                'id': i,
                'priority': priority,
                'duration': duration
            })
        
        # Initialize students with random preferences
        self.students = []
        for i in range(num_students):
            # Generate random availability (70% chance of being available)
            availability = np.where(np.random.random(num_time_slots) > 0.3)[0]
            
            # Generate random preferences between 0.5 and 2.0 for available slots
            preferences = {}
            for slot in availability:
                preferences[slot] = np.random.uniform(0.5, 2.0)
                
            self.students.append(Student(i, availability, preferences))

    def generate_assignments(self):
        population = []
        for _ in range(50):  # Population size
            schedule = []
            # Sort classes by priority (higher priority classes scheduled first)
            sorted_classes = sorted(self.classes, key=lambda x: x['priority'], reverse=True)
            for class_info in sorted_classes:
                time_slot = np.random.randint(0, self.num_time_slots)
                student = np.random.randint(0, self.num_students)
                schedule.append({
                    'class_id': class_info['id'],
                    'time_slot': time_slot,
                    'student': student
                })
            population.append(schedule)
        return population

    def draw_grid(self, screen, font, schedule):
        screen.fill((255, 255, 255))
        cell_width = 80
        cell_height = 60
        margin_left = 150
        margin_top = 100

        # Draw time slot headers
        for slot in range(self.num_time_slots):
            text = font.render(f"Slot {slot+1}", True, (0, 0, 0))
            screen.blit(text, (margin_left + slot * cell_width + 10, margin_top - 30))

        # Draw student preferences and grid
        for student in range(self.num_students):
            # Calculate average preference
            available_prefs = [self.students[student].get_preference(slot) 
                             for slot in self.students[student].availability]
            avg_pref = sum(available_prefs) / len(available_prefs) if available_prefs else 0
            
            pref_text = font.render(f"Preference: {avg_pref:.2f}", True, (0, 0, 0))
            screen.blit(pref_text, (10, margin_top + student * cell_height + cell_height // 3))

            for slot in range(self.num_time_slots):
                cell_rect = pygame.Rect(
                    margin_left + slot * cell_width,
                    margin_top + student * cell_height,
                    cell_width,
                    cell_height,
                )

                # Default color
                color = (200, 200, 200)  # Light gray for unassigned
                
                # Find class assignment for this slot and student
                assigned_class = None
                for assignment in schedule:
                    if assignment['time_slot'] == slot and assignment['student'] == student:
                        assigned_class = self.classes[assignment['class_id']]
                        if slot in self.students[student].availability:
                            # Blue if preferred (preference > 1.0), grey otherwise
                            color = (0, 0, 255) if self.students[student].get_preference(slot) > 1.0 else (200, 200, 200)
                        else:
                            # Red if slot is unavailable
                            color = (255, 0, 0)
                        
                        # Draw class information
                        priority_text = font.render(f"P{assigned_class['priority']}", True, (255, 255, 255))
                        duration_text = font.render(f"{assigned_class['duration']}h", True, (255, 255, 255))
                        screen.blit(priority_text, (cell_rect.x + 5, cell_rect.y + 5))
                        screen.blit(duration_text, (cell_rect.x + 5, cell_rect.y + 25))

                pygame.draw.rect(screen, color, cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)