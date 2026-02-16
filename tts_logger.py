# tts_logger.py
import logging
import statistics

# --------------------------
# Setup logger
# --------------------------
logging.basicConfig(
    filename="tts_metrics.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Store all latencies for reporting
first_chunk_latencies = []
total_latencies = []

def log_performance(sentence: str, tts_time_ms: float, total_time_ms: float, first_chunk_ms: float = None):
    """
    Logs TTS performance and tracks optimization metrics.

    :param sentence: Sentence being spoken
    :param tts_time_ms: Time spent in TTS generation
    :param total_time_ms: Total time including overhead
    :param first_chunk_ms: Time until first audio byte arrives
    """
    overhead_ms = total_time_ms - tts_time_ms

    # --------------------------
    # Terminal Output
    # --------------------------
    print("\n📊 PERFORMANCE REPORT")
    print(f"Sentence: {sentence}")
    if first_chunk_ms is not None:
        print(f"First Audio Chunk: {first_chunk_ms:.2f} ms")
        first_chunk_latencies.append(first_chunk_ms)
    print(f"TTS Generation Time: {tts_time_ms:.2f} ms")
    print(f"Total Time: {total_time_ms:.2f} ms")
    print(f"Overhead: {overhead_ms:.2f} ms")
    print("-" * 40)


    # --------------------------
    # File Logging
    # --------------------------
    log_message = f"Sentence='{sentence}' | TTS={tts_time_ms:.2f}ms | Total={total_time_ms:.2f}ms | Overhead={overhead_ms:.2f}ms"
    total_latencies.append(total_time_ms)

    if first_chunk_ms is not None:
        log_message += f" | FirstChunk={first_chunk_ms:.2f}ms"
    logging.info(log_message)

def log_summary():
    """
    Prints and logs overall optimization report at shutdown.
    """

    if not total_latencies:
        print("⚠️ No latency data collected.")
        return

    avg_total = statistics.mean(total_latencies)
    max_total = max(total_latencies)
    p95_total = statistics.quantiles(total_latencies, n=100)[94]

    print("\n📊 FINAL OPTIMIZATION SUMMARY")
    print("--------------------------------")
    print(f"Total Sentences Spoken : {len(total_latencies)}")
    print(f"Average Latency        : {avg_total:.2f} ms")
    print(f"Max Latency            : {max_total:.2f} ms")
    print(f"95th Percentile Latency: {p95_total:.2f} ms")
    print("--------------------------------")

    logging.info(
        f"FINAL SUMMARY: Avg={avg_total:.2f}ms | "
        f"Max={max_total:.2f}ms | P95={p95_total:.2f}ms"
    )
