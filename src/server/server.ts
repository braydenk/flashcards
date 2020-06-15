import express, { Request, Response } from 'express'

export default function initializeServer() {
  const app = express()

  // Express configuration
  app.set('port', process.env.PORT || 3000)

  app.get('/', (req: Request, res: Response) => {
    res.send('INDEX')
  })

  return app
}
