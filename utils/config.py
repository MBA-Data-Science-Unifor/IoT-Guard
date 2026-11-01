"""Constantes, caminhos e dicionários compartilhados entre as páginas."""
# --------------------------------------------------------------------- Nomes
NOMES = {
    "DOS_SYN_Hping": "DoS SYN",         "Thing_Speak": "ThingSpeak (normal)",
    "ARP_poisioning": "ARP poisoning",  "MQTT_Publish": "MQTT (normal)",
    "NMAP_UDP_SCAN": "Nmap UDP",        "NMAP_XMAS_TREE_SCAN": "Nmap XMAS",
    "NMAP_OS_DETECTION": "Nmap OS",     "NMAP_TCP_scan": "Nmap TCP",
    "DDOS_Slowloris": "DDoS Slowloris", "Wipro_bulb": "Wipro bulb (normal)",
    "Metasploit_Brute_Force_SSH": "Brute force SSH",
    "NMAP_FIN_SCAN": "Nmap FIN",
}

CORES = {"Normal": "#4C72B0", "Ataque": "#C44E52"}

CLASSES_NORMAIS = ["Thing_Speak", "MQTT_Publish", "Wipro_bulb"]
CLASSES_ATAQUE  = [
    "DOS_SYN_Hping", "ARP_poisioning", "NMAP_UDP_SCAN",
    "NMAP_XMAS_TREE_SCAN", "NMAP_OS_DETECTION", "NMAP_TCP_scan",
    "DDOS_Slowloris", "Metasploit_Brute_Force_SSH", "NMAP_FIN_SCAN",
]

# --------------------------------------------------------------------- Dataset
N_TOTAL        = 123_117
N_FEATURES_RAW = 85
N_FEATURES_ENC = 80
N_DUPLICADAS   = 5_195

DISTRIBUICAO_COMPLETA = {
    "DOS_SYN_Hping": 94_659, "Thing_Speak": 8_108,
    "ARP_poisioning": 7_750, "MQTT_Publish": 4_146,
    "NMAP_UDP_SCAN": 2_590,  "NMAP_XMAS_TREE_SCAN": 2_010,
    "NMAP_OS_DETECTION": 2_000, "NMAP_TCP_scan": 1_002,
    "DDOS_Slowloris": 534,   "Wipro_bulb": 253,
    "Metasploit_Brute_Force_SSH": 37, "NMAP_FIN_SCAN": 28,
}

DISTRIBUICAO_TREINO = {
    "DOS_SYN_Hping": 10_000, "Thing_Speak": 6_486, "ARP_poisioning": 6_200,
    "MQTT_Publish": 3_317,   "NMAP_UDP_SCAN": 2_072,
    "NMAP_XMAS_TREE_SCAN": 1_608, "NMAP_OS_DETECTION": 1_600,
    "NMAP_TCP_scan": 802,    "DDOS_Slowloris": 500,
    "Metasploit_Brute_Force_SSH": 500, "Wipro_bulb": 500, "NMAP_FIN_SCAN": 500,
}

DISTRIBUICAO_TESTE = {
    "DOS_SYN_Hping": 18_932, "Thing_Speak": 1_622, "ARP_poisioning": 1_550,
    "MQTT_Publish": 829,     "NMAP_UDP_SCAN": 518,
    "NMAP_XMAS_TREE_SCAN": 402, "NMAP_OS_DETECTION": 400,
    "NMAP_TCP_scan": 200,    "DDOS_Slowloris": 107,
    "Wipro_bulb": 51,        "Metasploit_Brute_Force_SSH": 7,
    "NMAP_FIN_SCAN": 6,
}

# --------------------------------------------------------------------- Benchmark
BENCHMARK = [
    {"Modelo": "RandomForest", "Acurácia": 0.997523, "Acur. balanceada": 0.974309,
     "Precisão macro": 0.942247, "Recall macro": 0.974309, "F1 macro": 0.955657,
     "F1 ponderado": 0.997535, "ROC-AUC (OvR)": 0.999683, "F1 macro (CV treino)": 0.984442,
     "Kappa": 0.993782, "MCC": 0.993783, "Log-Loss": 0.012012},
    {"Modelo": "HistGradientBoosting", "Acurácia": 0.997888, "Acur. balanceada": 0.979887,
     "Precisão macro": 0.936711, "Recall macro": 0.979887, "F1 macro": 0.954524,
     "F1 ponderado": 0.997912, "ROC-AUC (OvR)": 0.999941, "F1 macro (CV treino)": 0.982161,
     "Kappa": 0.994699, "MCC": 0.994700, "Log-Loss": 0.008424},
    {"Modelo": "LightGBM", "Acurácia": 0.997888, "Acur. balanceada": 0.972351,
     "Precisão macro": 0.936250, "Recall macro": 0.972351, "F1 macro": 0.950775,
     "F1 ponderado": 0.997909, "ROC-AUC (OvR)": 0.999968, "F1 macro (CV treino)": 0.984373,
     "Kappa": 0.994699, "MCC": 0.994700, "Log-Loss": 0.009518},
    {"Modelo": "Baseline (sempre DoS)", "Acurácia": 0.7688, "Acur. balanceada": 0.0833,
     "Precisão macro": 0.0641, "Recall macro": 0.0833, "F1 macro": 0.0724,
     "F1 ponderado": 0.6684,   "ROC-AUC (OvR)": None,   "F1 macro (CV treino)": None,
     "Kappa": 0.0, "MCC": 0.0, "Log-Loss": None},
]

BEST_MODEL_NAME = "RandomForest"
BEST_MODEL_PARAMS = {
    "class_weight": "balanced_subsample",
    "max_depth": None,
    "max_features": "sqrt",
    "min_samples_leaf": 1,
    "n_estimators": 400,
}

TOP_FEATURES_MI = [
    "fwd_pkts_payload.avg", "fwd_pkts_payload.max", "fwd_subflow_bytes",
    "flow_pkts_payload.tot", "fwd_pkts_payload.tot", "flow_pkts_payload.avg",
    "flow_pkts_payload.max", "id.resp_p",
    "fwd_last_window_size", "fwd_init_window_size",
]

TOP_SCORES_MI = [0.8635, 0.8584, 0.8531, 0.8503, 0.8474,
                 0.8456, 0.8445, 0.7981, 0.7676, 0.6999]
