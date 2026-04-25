# Flee Behavior – Analysis

## Objective
Implement a system where smaller squares move away from larger ones while keeping random motion.

## Approach
Each square:
- Loops through all other squares
- Identifies larger squares as threats
- Computes direction away from threat
- Applies a force proportional to distance

## Key Concepts
- Distance formula
- Vector normalization
- Force accumulation
- Velocity limiting

## Behavior Design
- Squares only react within a radius (FLEE_RADIUS)
- Closer threats produce stronger fleeing force
- Random jitter is added to prevent predictable motion

## Edge Cases
- Ignore self comparison
- Avoid division by zero
- Ignore equal or smaller squares
- Combine multiple flee forces

## Parameters
- FLEE_RADIUS controls detection range
- FLEE_FORCE controls escape strength
- JITTER adds randomness

## Result
The system produces natural-looking motion where:
- Small squares avoid large ones
- Movement remains dynamic and non-linear