import initializeServer from './server'

const app = initializeServer()

const server = app.listen(app.get('port'), () => {
  console.log(`
    Listening on port ${app.get('port')}

    Press CTRL-C to stop\n
  `)
})

export default server
