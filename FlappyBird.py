import os

import neat
import pygame

from CreateGame import Bird, Ground, Pipe, WIDTH, HEIGHT, draw_window

def main(genomes, config):
    nets = []
    genome = []
    birds = []

    for genomeId, gene in genomes:
        net = neat.nn.FeedForwardNetwork.create(gene, config)
        nets.append(net)
        gene.fitness = 0
        genome.append(gene)
        birds.append(Bird(230, 350))

    ground = Ground(730)
    pipes = [Pipe(600)]
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    score = 0
    while True:
        # At most 30 iterations every second
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pipe_index = 0
        if len(birds) <= 0:
            break
        else:
            # Checks if we have to target the second pipe based on if the bird has passed the first pope
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1

        for x, bird in enumerate(birds):
            bird.move()
            genome[x].fitness += 0.1
            result = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_index].height)
                                       , abs(bird.y - pipes[pipe_index].bottom)))
            if result[0] > 0.5:
                bird.jump()

        temp = []
        add_pipe = False
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    genome[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    genome.pop(x)

                if pipe.passed or pipe.x >= bird.x:
                    continue
                # As soon as the bird passes through a pipe, we have to add a new pipe
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                temp.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for gene in genome:
                gene.fitness += 5

            pipes.append(Pipe(600))

        for pipe in temp:
            pipes.remove(pipe)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                genome[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                genome.pop(x)

        ground.move()
        draw_window(window, birds, pipes, ground, score)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
