/**
 * Angular generates an environment.ts and an environment.development.ts when the ng generate environments command is run
 * According to the angular.json configurations, this file is meant to be treated as the production environment whereas
 * environment.development.ts is meant to be treated as the dev environment
 * 
 * tldr:
 *  ng serve uses environment.development.ts
 *  ng build uses environment.ts
 * 
 */

export const environment = {
  production: true,
  apiUrl: 'dev-alb-833559820.us-east-1.elb.amazonaws.com'
};