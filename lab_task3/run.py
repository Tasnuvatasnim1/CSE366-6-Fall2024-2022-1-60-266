import pygame 
import numpy as np
from environment import Environment
import random

def fitness(schedule, environment):
    total_score = 100.0  # Start with maximum score
    
    # Track assigned slots per student to check for overlapping
    assigned_slots = {student: {} for student in range(environment.num_students)}
    
    # Sort schedule by class priority
    sorted_schedule = sorted(schedule, 
                           key=lambda x: environment.classes[x['class_id']]['priority'],
                           reverse=True)
    
    for assignment in sorted_schedule:
        time_slot = assignment['time_slot']
        student = assignment['student']
        class_info = environment.classes[assignment['class_id']]
        student_obj = environment.students[student]
        
        # Priority-based scoring
        priority_weight = class_info['priority'] / 5.0  # Normalize priority
        
        # Add points for correct placement
        if time_slot in student_obj.availability:
            # Add points based on student preference
            preference = student_obj.get_preference(time_slot)
            total_score += preference * priority_weight * 10
        else:
            # Deduct points for unavailable slots
            total_score -= 20.0 * priority_weight
            
        # Check for overlapping classes
        for t in range(time_slot, time_slot + class_info['duration']):
            if t in assigned_slots[student]:
                total_score -= 30.0 * priority_weight  # Heavy deduction for overlaps
            assigned_slots[student][t] = assignment['class_id']
            
    return max(0, total_score)  # Ensure score doesn't go negative

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    return child

def mutate(schedule, environment, mutation_rate=0.2):
    if random.random() < mutation_rate:
        idx = random.randint(0, len(schedule) - 1)
        schedule[idx] = {
            'class_id': schedule[idx]['class_id'],
            'time_slot': random.randint(0, environment.num_time_slots - 1),
            'student': random.randint(0, environment.num_students - 1)
        }
    return schedule

def run_scheduler():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Class Schedule Optimization")
    font = pygame.font.Font(None, 24)

    num_classes = 10
    environment = Environment(num_classes)
    population = environment.generate_assignments()
    
    generation_count = 0
    best_fitness = 0  # Initialize to minimum possible fitness
    max_fitness_achieved = 0  # Track maximum fitness achieved
    running = True
    
    while running and generation_count < 100:  # 100 generations
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Evolution step
        # Sort by fitness in descending order (higher is better)
        ranked_population = sorted(population, 
                                 key=lambda x: fitness(x, environment),
                                 reverse=True)  # Changed to reverse=True
        parents = ranked_population[:25]  # Top 50%
        
        next_gen = []
        for _ in range(50):  # Maintain population size
            parent1, parent2 = random.choices(parents, k=2)
            child = mutate(crossover(parent1, parent2), environment)
            next_gen.append(child)
            
        population = next_gen
        
        # Display current best solution
        current_best = max(population,  # Changed to max
                         key=lambda x: fitness(x, environment))
        current_fitness = fitness(current_best, environment)
        max_fitness_achieved = max(max_fitness_achieved, current_fitness)  # Track maximum
        
        # Update display
        environment.draw_grid(screen, font, current_best)
        
        gen_text = font.render(f"Generation: {generation_count + 1}", True, (0, 0, 0))
        fit_text = font.render(f"Best Fitness (Current): {current_fitness:.2f}", True, (0, 0, 0))
        max_fit_text = font.render(f"Max Fitness Achieved: {max_fitness_achieved:.2f}", True, (0, 0, 0))
        
        screen.blit(gen_text, (900, 50))
        screen.blit(fit_text, (900, 80))
        screen.blit(max_fit_text, (900, 110))
        
        pygame.display.flip()
        pygame.time.delay(500)  # 500ms delay between generations
        generation_count += 1
        
    pygame.quit()

if __name__ == "__main__":
    run_scheduler()