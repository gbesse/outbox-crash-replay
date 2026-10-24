# outbox-crash-replay

## Français

Tuer un vrai processus SQLite pour tester les frontières d’une outbox.

Données fictives ; aucun accès réseau ni secret requis.

```sh
python -m outbox_crash_replay examples/demo.json --lang fr
python -m unittest discover -s tests -v
```

### Méthode et différence

Tue réellement un processus aux points avant commit, après commit et après livraison avant accusé. Deux bases SQLite séparées rendent le doublon observable et montrent l’effet d’un consommateur idempotent.

### Limites

Sous-processus POSIX fixes et fichiers temporaires possédés, sans réseau. SIGKILL de processus, pas panne électrique, stockage distribué ni preuve de livraison exactement une fois.

### Validation

Tests de domaine, cas limites et interface FR/EN/ES. La CI teste Python 3.11/3.13 et exécute la wheel installée hors du checkout. JSON conserve les identifiants techniques et les données fournis. Erreur d’entrée : code de sortie 2.

## English

Kill an actual SQLite process to test outbox boundaries.

Synthetic data; no network access or secret required.

```sh
python -m outbox_crash_replay examples/demo.json --lang en
python -m unittest discover -s tests -v
```

### Method and difference

Actually kills a process before commit, after commit and after delivery before acknowledgement. Separate SQLite databases make duplication observable and show the effect of an idempotent consumer.

### Limits

Fixed POSIX subprocesses and owned temporary files, no network. Process SIGKILL, not power loss, distributed storage or exactly-once delivery proof.

### Validation

Domain tests, boundary cases and FR/EN/ES interface. CI tests Python 3.11/3.13 and runs the installed wheel outside the checkout. JSON preserves technical identifiers and supplied data. Invalid input exits with code 2.

## Español

Matar un proceso SQLite real para probar límites de una outbox.

Datos sintéticos; no requiere red ni secretos.

```sh
python -m outbox_crash_replay examples/demo.json --lang es
python -m unittest discover -s tests -v
```

### Método y diferencia

Mata realmente un proceso antes del commit, después y tras entrega antes de confirmación. Bases SQLite separadas hacen visible duplicación y efecto del consumidor idempotente.

### Límites

Subprocesos POSIX fijos y archivos temporales propios, sin red. SIGKILL de proceso, no corte eléctrico, almacenamiento distribuido o prueba de entrega exactamente una vez.

### Validación

Pruebas de dominio, casos límite e interfaz FR/EN/ES. CI prueba Python 3.11/3.13 y ejecuta la wheel instalada fuera del repositorio. JSON conserva identificadores técnicos y datos proporcionados. Entrada inválida termina con código 2.

## Sources / Fuentes

- https://www.sqlite.org/atomiccommit.html
- https://microservices.io/patterns/data/transactional-outbox.html
