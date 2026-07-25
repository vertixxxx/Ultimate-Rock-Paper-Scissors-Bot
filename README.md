# Adaptive AI for Rock, Paper, Scissors

An exploration of statistical and probabilistic machine learning models applied to game strategy. This project transitions from baseline random selection to adaptive prediction models capable of detecting human pattern bias and dynamic strategy shifts in real time.

---

## Model Architectures

### 1. Baseline Model (`RandomBot`)
* **Type:** Uniform Random Strategy
* **Logic:** Selects moves with uniform probability ($P = \frac{1}{3}$) across all options.
* **Purpose:** Establishes a zero-memory baseline to validate that higher-order models perform statistically better than chance.

---

### 2. First-Order Markov Chain (`Markov1`)
* **Type:** State Transition Frequency Model (Order 1)
* **State Space:** Single previous player move $S_t = M_{t-1}$
* **Logic:** Tracks the empirical transition frequencies of player moves given their immediately preceding choice.

$$\hat{P}(M_t \mid M_{t-1}) = \frac{C(M_{t-1} \to M_t)}{\sum_{m} C(M_{t-1} \to m)}$$

* **Limitation:** Fails to capture multi-turn sequences or strategic shifts, and susceptible to zero-frequency errors on unobserved state transitions.

---

### 3. Second-Order Markov Chain (`Markov2`)
* **Type:** Higher-Order State Transition Model (Order 2)
* **State Space:** Sequence of two preceding player moves $S_t = (M_{t-2}, M_{t-1})$
* **Logic:** Increases contextual awareness by tracking transition probabilities over longer historical sequences.

$$\hat{P}(M_t \mid M_{t-2}, M_{t-1}) = \frac{C(M_{t-2}, M_{t-1} \to M_t)}{\sum_{m} C(M_{t-2}, M_{t-1} \to m)}$$

* **Limitation:** Requires larger sample sizes to populate the expanded state space ($3^2 = 9$ states). Slower to adapt if the human player changes tactics mid-game.

---

### 4. Bayesian Markov Chain with Exponential Decay (`BayesianMarkov`)
* **Type:** Dirichlet Prior Distribution with Memory Decay
* **State Space:** Order-2 State Context $S_t = (M_{t-2}, M_{t-1})$
* **Logic:** Combines Laplace smoothing with a discount factor to balance stability on small sample sizes with rapid adaptability against strategy changes.

#### Dirichlet Prior Initialization
Every unobserved state is initialized with a uniform prior $\boldsymbol{\alpha} = (1.0, 1.0, 1.0)$ to model initial uncertainty without falling back to random selection or overestimating single-observation events.

$$\mathbb{E}[P(M_t = m \mid S_t)] = \frac{\alpha_m}{\sum_{k} \alpha_k}$$

#### Exponential Memory Decay
Before registering an observed player move at time $t$, past evidence counts within the active state are discounted using decay factor $\gamma = 0.95$:

$$\alpha_{m, t} = \gamma \cdot \alpha_{m, t-1} + \mathbb{I}(M_t = m)$$

Where $\mathbb{I}$ is an indicator function evaluating to $1$ for the observed move and $0$ otherwise.

---

## Model Comparison Matrix

| Feature | Random | Order-1 Markov | Order-2 Markov | Bayesian Markov |
| :--- | :--- | :--- | :--- | :--- |
| **History Context** | 0 Turns | 1 Turn | 2 Turns | 2 Turns |
| **Prior Distribution** | None | None | None | Uniform Dirichlet $\boldsymbol{\alpha}=(1,1,1)$ |
| **Adapts to Mid-Game Changes** | N/A | Slow | Very Slow | Fast ($\gamma = 0.95$) |
| **Small Sample Stability** | Low | Low (Overfits) | Very Low (Overfits) | High (Smoothed) |

---

## Installation & Usage

### Prerequisites
* Python 3.8+
* Pygame

### Running the Project
```bash
python main.py
