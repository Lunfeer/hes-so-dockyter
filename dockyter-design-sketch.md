# Dockyter – Design Sketch (Draft)

Semester project: **Dockyter – Jupyter magics to run Docker containers**

This document summarizes an initial design for Dockyter: an IPython/Jupyter extension that adds a `%%docker` magic and routes shell commands through Docker.

---

## 4.1 Use cases

- **Run CLI tools packaged only as Docker images**  
  Users can keep the Python kernel light and offload heavy tools to separate images.

- **Keep notebook environments small and focused**  
  Instead of installing every big tools in the projetct docker image, Dockyter runs them in dedicated containers.

- **Binder / JupyterHub workflows**  
  In deployments where the notebook server already runs in a container (Binder, DockerSpawner on JupyterHub), Dockyter provides a controlled way to launch extra containers from notebooks.

---

## 4.2 User-facing syntax

Proposed minimal interface:

```python
%%docker [DOCKER-RUN-ARGS...] IMAGE[:TAG]
```

Examples (informal):

* `%%docker -v /home/jovyan/data:/input myorg/tool:1.0`
  → configure Dockyter to use this image and arguments.

Once configured, lines starting with `!` are executed as:

```bash
docker run --rm [DOCKER-RUN-ARGS...] IMAGE[:TAG] bash -lc "<original !command>"
```

Basic rules:

* Only `!` commands are routed through Docker; normal Python cells are unaffected.
* Config can be reset with something like `%docker_off`.
* Arguments should follow the classic `docker run` semantics: volumes (`-v`), env vars (`-e`), etc...

---

## 4.3 Architecture options

### A. IPython extension (starting point)

* Implement `%%docker`, `%docker_off`, etc... in a magics class, as described in the IPython magics docs and discourse 3.
* Pros: easy to ship as a separate package, works in any IPython-based kernel.
* Cons: have to modify `InteractiveShell.system` to route correclty `!cmd`. That can be fragile...
* Security: Can filters (images, flags...) in the Dockyter code full Python/system accèss, so it’s not safe for untrusted users.

### B. Inclusion in ipykernel

* Move the extension (at least the logic) into ipykernel.
* Pros: consistent behaviour across frontends; easier to control in JupyterHub/Binder deployments.
* Cons: more coordination with upstream. Heavier review and maintenance...
* Security: Same in-kernel limits, but Dockyter can be centrally enabled/disabled and configured via kernel settings, which helps in multi-user JupyterHub/Binder deployments.

### C. Separate “Docker-aware” kernel

* Provide a dedicated kernel that always uses Dockyter.
* Pros: clear separation of responsibilities; predictable behaviour for admins.
* Cons: extra kernel to maintain. Less flexible than a simple `%load_ext`.
* Security: Still arbitrary Python inside, but this kernel can be isolated and restricted at the infrastructure level (reserve this kernel only for this user/groupe), making it the easiest to lock down in production.

---

## 4.4 Docker interaction

Two main options:

* **Call Docker CLI (`docker run ...`)**

  * Simple, no extra Python dependencies, reuses user’s Docker config.
  * Good for a first prototype; error handling via process return.

* **Use Docker Engine API / Python SDK**

  * More control over containers (logs, lifecycle, resource limits).
  * Better for advanced features, but adds dependencies and configuration overhead.

For the first iteration of Dockyter, using the Docker CLI is likely enough.

---

## 4.5 Open questions

Some design questions to keep track of:

* **Security / policies**

  * How to restrict dangerous flags (`--privileged`, host mounts)?
  * How can admins completely disable Dockyter in locked-down environments ?

* **Environments without Docker**

  * What happens if `docker` is not installed or accessible (e.g. some Binder setups)?

* **Lifecycle and performance**

  * Are containers always short-lived (`docker run --rm`) or can users keep them running?
  * How to avoid overloading shared infrastructure with too many parallel containers?

* **Integration with kernels**

  * How to make Dockyter play nicely with kernel architecture and message flow ?
  * How to expose or hide Dockyter in different Binder/JupyterHub profiles?