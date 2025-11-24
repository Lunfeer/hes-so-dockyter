# Dockyter – Onboarding & First-Day Tasks

Semester Project: **Dockyter – Jupyter magics to run Docker containers**

---

## 0. Big-picture goal (for you)

By the end of today, you should:

1. Have a rough mental model of how Jupyter, kernels, magics, and Docker fit together.  
2. Know what the community has already tried or discussed.  
3. Have a **first design sketch** for a `%%docker` magic that could live as a reusable extension (not only inside `ipykernel`).  

Deliverables for today are in section 5.

---

## 1. Environment & repo setup

1. Make sure you have:
   - A recent Python (3.10+ recommended).
   - Docker installed and working (`docker run hello-world`).
2. [Fork the IPykernel project](https://github.com/ipython/ipykernel/fork)
3. Clone your fork of the `ipykernel` repo and install it in editable mode in a fresh virtual environment:
   ```bash
   git clone https://github.com/<your-gh-user>/ipykernel.git
   cd ipykernel
   pip install -e ".[test]"
   ```
4. Verify you can start a notebook using this local kernel and run a simple cell.

---

## 2. Jupyter Community Forum research (Discourse)

1. [Fork this project](https://github.com/oesteban/hes-so-dockyter/fork)
2. Head to [the Jupyter Community forum](https://discourse.jupyter.org/) and research **at least 10 discussions** on Docker, Binder, kernels, magics, or security relevant to this project.
3. In your fork of this project, create a branch called "preliminary-research" and switch to it.
4. Create a file called `discourse-topics.md` at the top of the repo. Add all the relevant topics from the forum, as a table like this:
   ```markdown
   | # | Link | Category | One-line summary | Relevance to Dockyter |
   ```

---

## 3. Investigate how magics actually work

1. Explore built‑in magics:  
   ```python
   %lsmagic
   %magic
   ```
2. Inspect magics like `%matplotlib`, `%%bash`, `%%timeit`.
3. Implement a small custom magic using an IPython extension:

```python
# mymagics.py
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)

@magics_class
class MyMagics(Magics):
    @line_magic
    def hello(self, line):
        print(f"Hello: {line}")

    @cell_magic
    def echo(self, line, cell):
        print(f"Line: {line}")
        print(cell)

def load_ipython_extension(ip):
    ip.register_magics(MyMagics)
```

This will be the base for the future `%%docker` magic.

---

## 4. Draft the first design for Dockyter

Create: `dockyter-design-sketch.md`

Include:

### 4.1. Use cases  
Examples:
- running CLI tools packaged only as Docker images  
- keeping notebook environments lightweight  
- Binder/JupyterHub compute workflows  

### 4.2. User-facing syntax  
Example:

```
%%docker -v /home/jovyan/data:/input image:latest
!tool --input /input/file.txt
```

Define how arguments, images, mounts, env vars and cell behavior work.

### 4.3. Architecture options  
Compare:
- IPython extension (recommended starting point)  
- inclusion in ipykernel  
- separate kernel  

List pros/cons, security implications, deployment considerations.

### 4.4. Docker interaction questions  
Decide between:
- calling Docker CLI  
- using Docker Engine API  

Consider log streaming, error handling, sandboxing.

### 4.5. Open questions  
Make a list (e.g., Binder behavior, disabled Docker environments, mixing Python and shell code).

---

## 5. Post a project question on Discourse

Draft and publish a topic describing Dockyter and asking for design guidance. Include:

- project context  
- example of intended `%%docker` usage:
   ```
   %%docker -v /home/jovyan/data:/input image:latest
   !tool --input /input/file.txt
   ```
- architectural questions  
- security considerations

Save the URL of your post in your notes.

---

## 6. Optional follow‑up explorations

Scan related tools:
- repo2docker  
- Jupyter Docker Stacks  
- dockerspawner  
- any prior Docker magic attempts  

---

## 7. End-of-day checklist

- [ ] 10+ Discourse topics researched  
- [ ] Discourse post published  
- [ ] `dockyter-design-sketch.md` created  
- [ ] Minimal custom IPython magic implemented  
