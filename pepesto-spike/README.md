# Pepesto Spike
A little spike script to run an end-to-end flow of Pepesto.

Gets up to the step of submitting the order, which will require us to have a session on a web browser / playwright that we control.

To run, create a .env file and insert `PEPESTO_KEY=<our pepesto key>` and run `node index.js`.

Results are written to the `results/` directory. 

Please don't run this loads and loads of times - we have limited credits!