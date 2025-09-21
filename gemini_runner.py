import multiprocessing
import uvicorn
from gemini_player_factory import create_app

def run_server(model_id, port):
	app = create_app(model_id)
	uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
	configs = [
		("gemini-2.0-flash-lite", 8002),
		("gemini-2.0-flash", 8001),
		# Add more (model_id, port) pairs as needed
	]
	processes = []
	for model_id, port in configs:
		p = multiprocessing.Process(target=run_server, args=(model_id, port))
		p.start()
		processes.append(p)
	for p in processes:
		p.join()