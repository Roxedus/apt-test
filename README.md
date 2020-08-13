# Ombi APT repo

## Master (currently blank)

```bash
curl -sSL https://roxedus.github.io/apt-test/pub.key | sudo apt-key add -
echo "deb https://roxedus.github.io/apt-test/master jessie main" | tee /etc/apt/sources.list.d/ombi.list
```

## Develop (Currently v4 beta)

```bash
curl -sSL https://roxedus.github.io/apt-test/pub.key | sudo apt-key add -
echo "deb https://roxedus.github.io/apt-test/develop jessie main" | tee /etc/apt/sources.list.d/ombi.list
```
