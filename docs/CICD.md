# CI/CD

## Continuous integration

### Build

| Permissions  | Triggers       |
| ------------ | -------------- |
| Read / Write | Push to `main` |



```mermaid
stateDiagram-v2
	direction LR
	
	[*] --> Test
	Test --> Versioning
	Versioning --> Build
	Build --> Packages
	Build --> Releases
	state release_state <<join>>
	Releases --> release_state
	Packages --> release_state
	release_state --> Deploy_webhook
	Deploy_webhook --> [*]
```

### Coverage

| Permissions | Triggers       |
| ----------- | -------------- |
| Read only   | Push to `main` |

```mermaid
stateDiagram-v2
	direction LR
	
	[*] --> Test
	Test --> Build
	Build --> Coverage
	Coverage --> [*]
	
```



## Continuous delivery

| Permissions | Triggers                               |
| ----------- | -------------------------------------- |
| Read only   | Package created (triggered by webhook) |

```mermaid
stateDiagram-v2
	direction LR
	
	[*] --> Apply_deployment
    Apply_deployment --> [*]
```

