# Doc Build Instructions


1. Start virtual Python environment: `.venv/bin/activate`
2. Run build and review script: `./checkwork.sh`

   ```
   make clean
   make html
   cd _build/html
   python3 -m http.server
   ```

3. Review in browser: [http://localhost:8000](http://localhost:8000)
4. Exit simple web server: `ctrl-c`