import os
import subprocess
import time
import psutil

def get_cpu_times():
    cpu_times = psutil.cpu_times()
    return cpu_times.user, cpu_times.system

def run_program():
    cpu_quota = float(input("Informe a quota de tempo de CPU (em segundos): "))
    while True:
        binary = input("Informe o nome do binário a ser executado: ")
        timeout = float(input("Informe o tempo limite para a execução (em segundos): "))
        
        # Tempo de CPU inicial
        user_time_start, system_time_start = get_cpu_times()
        
        start_time = time.time()
        process = subprocess.Popen(binary, shell=True)
        
        while process.poll() is None:
            elapsed_time = time.time() - start_time
            
            # Verificar o tempo de CPU usado até agora
            user_time_current, system_time_current = get_cpu_times()
            cpu_time_used = (user_time_current - user_time_start) + (system_time_current - system_time_start)
            
            if elapsed_time >= timeout:
                process.kill()
                print(f"O processo {binary} foi morto após exceder o tempo limite de {timeout} segundos.")
                break
            
            if cpu_time_used >= cpu_quota:
                process.kill()
                print(f"O processo {binary} foi morto após exceder a quota de tempo de CPU de {cpu_quota} segundos.")
                break
            
            time.sleep(0.1)  # Aguarda 100ms antes de checar novamente
        
        # Se o processo terminou normalmente, calcular o tempo de CPU total usado
        if process.poll() is not None:
            user_time_end, system_time_end = get_cpu_times()
            cpu_time_used = (user_time_end - user_time_start) + (system_time_end - system_time_start)
            elapsed_time = time.time() - start_time
            print(f"O processo {binary} terminou em {elapsed_time:.2f} segundos.")
            print(f"Tempo de CPU usado: {cpu_time_used:.2f} segundos.")
        
        # Verificar se a quota de tempo de CPU foi excedida
        if cpu_time_used >= cpu_quota:
            print(f"A quota de tempo de CPU de {cpu_quota} segundos foi excedida.")
            break

if __name__ == "__main__":
    run_program()
