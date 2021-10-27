### https://mozilla.github.io/mozillavpn-product-details

Hosts a [product-details](https://github.com/mozilla-releng/product-details) style json files for the vpn.

Automatically deploys to gh pages.

#### Enforced restrictions
* No pushing to main
* Codeowners must approve production file changes
* Commits must be signed
* No exceptions

#### Running locally

```sh
npm i
npm test
```
