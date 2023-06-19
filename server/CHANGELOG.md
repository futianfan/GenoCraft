# Change Log

## [v1.0.7] 2023-02-11
### Changes

- Codebase Improvements
- `DB Management` Improvement
  - `Silent fallback` to **SQLite**

## [v1.0.6] 2022-12-08
### Changes

- OAuth via Github (stable)

## [v1.0.5] 2022-12-02
### Changes

- Minor Improvements
- Tests for React Kits

## [v1.0.4] 2022-11-13
### Improvements

- Added `deployer` file
  - Used by AppSeed [Go-LIVE](https://appseed.us/go-live/) service
  
## [1.0.3] 2022-11-05
### Improvements

- Updated for Deploy on RENDER using [Python Deployer](https://github.com/app-generator/deploy-automation-render)
  - `python.exe .\deployer.py flask https://github.com/app-generator/api-server-flask`
  - The new API is usable via `https://api-server-flask-<RANDOM>.onrender.com/api/`

## [1.0.2] 2022-06-07
### Improvements

- Update dependencies 

## [1.0.1] 2021-11-16
### Improvements

- Tables automatic creation
- Dependencies Update:
  - Flask==2.0.2
  - flask-restx==0.5.1
- Docker Scripts   

## [1.0.0] 2021-07-20
### Stable release

- Persistance: SQLite3  
- Stack: Flask / Flask-JWT-Extended / SQLAlchemy
- API:
   - Sign UP: `/api/users/register`
   - Sign IN: `/api/users/login`
   - Logout: `/api/users/logout`

