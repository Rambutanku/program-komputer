import os

import kagglehub
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import base64

ICON_B64 = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAA6lBMVEVHcEz/AAD/AAD/AAD/AAD/AAD+AAD5AAD8AAD/AAD/AAD/AAD/AAD/AADSAAD9AAD0AADvAAD3AAD6AADIAAD/AADPAAD/AADSAAD/AAD/AAD+AADcAAD/AAD/AADjAAD1AAD/AAD/AAD/AAD+AAD/AADjAAD7AAD8AAD/AAD/AAD9AAD/AAD/AAD+AAD/AAD/AACQAAABAAD+AACbKAC0AAD9AAAA2QD////8AACzAACwVwz/wv8A+QAAaQDWAADlAAAA0gAAggD6AAD7AADFAADLAADgAADnAADKAACyAADjAAD7BQWbVwAZlqccAAAAMHRSTlMACQYMV1TvWlau+vzc95LqYV5bkbDmle6Zxe3utInXEmdZssf6UQmPuBKN6VurtFAhHxmFAAABpElEQVQ4y4VTiVbbQAzchAQCBXpQoOWmN5RDs6dNYnOUq9f//04l2SYJTWDe867tGY2ktWxMg1SmVGRZv29gJiClVJZlKoq/UwSiSOnqqkzTBAIUxeXTgtPuZdE/xAzf4n9ZuzsPIvpDtLOPCYIZgERAjoB5pb3nxVq1a3ffVzQDjt8cVLQoNDuHc6D33nmvDw1dC9h/nc39KgnldWnqsKLYFuvoZjXFpvA16yuL9gd2da4qweUbfA86bpvawpjPUh/gFlnjRCidPHRqrYRrf4wFFx3NOvpOdFSdHtiiI2fATGYzR7zQuIe1HXmuasgpShquGCcc7WuF2IOvFzFSfBndEgto5LQ7QkKNnYu6s0APoP6MgVRgoyjYUHuxtpYArRBwjfqdJswJI7wxbwPwg20Zg8EnNojMzg0PM3t9A9ze59LGYMC82IyNREubRi6pNRr4uDs6a4qAEM5/X1xIkYS5sWE0rZXzM4RfoQa+9R5PXOsN7vDzjME+4euEmQXX8Wp57d3Wnu19UddHfDNcvE36MdDM1jSBGRoY658TTOPt+F7hH6SZazOFUAaPAAAAAElFTkSuQmCC"

st.set_page_config(
    page_title="Dashboard Forensik Judi Online 2026",
    page_icon=base64.b64decode(ICON_B64),
    layout="wide",
)

sns.set_theme(style="whitegrid", palette="muted")

KATEGORI_JUDI_ONLINE = [
    "Dormant-Takeover-Syndicate",
    "Direct-Gambling-Collector-Mule",
    "Layering-Mule-Account",
]

DATASET_URL = (
    "https://www.kaggle.com/datasets/luthfimuthathohirin/"
    "indonesia-online-gambling-bank-accounts-forensics"
)

BIBTEX = """@dataset{muthathohirin2026online_gambling_forensics,
  author       = {Luthfi Muthathohirin},
  title        = {Indonesia Online Gambling Transactions and Money Mule Accounts: 2026 Forensic Benchmark},
  year         = {2026},
  publisher    = {Kaggle},
  url          = {https://www.kaggle.com/datasets/luthfimuthathohirin/indonesia-online-gambling-bank-accounts-forensics},
  license      = {Creative Commons Zero v1.0 Universal}
}"""


@st.cache_data(show_spinner="Mengunduh dan memuat dataset...")
def load_data():
    path = kagglehub.dataset_download(
        "luthfimuthathohirin/indonesia-online-gambling-bank-accounts-forensics"
    )
    csv_files = [f for f in os.listdir(path) if f.endswith(".csv")]
    df = pd.read_csv(os.path.join(path, csv_files[0]))
    return df


df = load_data()

st.title("Dashboard Forensik Rekening Money Mule Judi Online 2026")
st.caption(
    "Dataset: Indonesia Online Gambling Bank Accounts Forensics (Kaggle). "
    "Data bersifat sintetis (benchmark riset yang dikalibrasi terhadap tipologi "
    "forensik publik PPATK, BI, OJK) — bukan data transaksi perbankan riil."
)

with st.sidebar:
    st.header("Filter Analisis")
    selected_risk = st.multiselect(
        "Klasifikasi risiko (subset terindikasi judi online)",
        options=KATEGORI_JUDI_ONLINE,
        default=KATEGORI_JUDI_ONLINE,
    )
    selected_institution = st.multiselect(
        "Jenis institusi",
        options=sorted(df["institution_type"].unique()),
        default=sorted(df["institution_type"].unique()),
    )
    st.markdown("---")
    st.markdown(
        "**Pertanyaan bisnis:**\n"
        "1. Kombinasi kanal x KYC paling berisiko\n"
        "2. Institusi dengan eksposur risiko tertinggi\n"
        "3. Indikator anomali paling dominan\n"
        "4. Kalibrasi ambang skor AML\n"
        "5. Profil risiko per kelompok usia\n"
        "6. Sinyal perangkat untuk auto-flag\n"
        "7. Durasi dana & micro-deposit"
    )
    st.markdown("---")
    with st.expander("Sumber Data & Sitasi"):
        st.markdown(
            "**Dataset:** Indonesia Online Gambling Transactions and Money Mule "
            "Accounts: 2026 Forensic Benchmark  \n"
            "**Author:** Luthfi Muthathohirin (2026)  \n"
            "**Publisher:** Kaggle  \n"
            "**Lisensi:** Creative Commons Zero v1.0 Universal  \n"
            f"**URL:** [Kaggle — Indonesia Online Gambling Bank Accounts Forensics]({DATASET_URL})"
        )
        st.code(BIBTEX, language="bibtex")

if not selected_risk:
    st.warning("Pilih minimal satu klasifikasi risiko untuk memulai analisis.")
    st.stop()

high_risk_df = df[
    df["account_risk_classification"].isin(selected_risk)
    & df["institution_type"].isin(selected_institution)
].copy()
df_filtered = df[df["institution_type"].isin(selected_institution)].copy()

if high_risk_df.empty:
    st.warning("Tidak ada rekening yang cocok dengan kombinasi filter saat ini.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rekening", f"{len(df_filtered):,}")
col2.metric("Rekening Terindikasi Judi Online", f"{len(high_risk_df):,}")
col3.metric(
    "Proporsi Berisiko",
    f"{len(high_risk_df) / len(df_filtered) * 100:.1f}%",
)
col4.metric(
    "Rata-rata Passthrough Velocity",
    f"{high_risk_df['passthrough_velocity_pct'].mean():.2f}%",
)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "Pertanyaan 1 — Kanal x KYC",
        "Pertanyaan 2 — Institusi",
        "Pertanyaan 3 — Indikator Anomali",
        "Pertanyaan 4 — Ambang Skor",
        "Pertanyaan 5 — Profil Usia",
        "Pertanyaan 6 — Perangkat",
        "Pertanyaan 7 — Dana & Micro-Deposit",
    ]
)

with tab1:
    st.subheader("Kombinasi kanal transaksi x status KYC paling berisiko")

    channel_kyc_agg = (
        high_risk_df.groupby(
            ["primary_transaction_channel", "kyc_verification_status"], observed=True
        )
        .agg(
            n_accounts=("account_id", "count"),
            avg_late_night_pct=("late_night_transaction_ratio", "mean"),
            avg_passthrough_pct=("passthrough_velocity_pct", "mean"),
        )
        .reset_index()
    )

    metric_choice = st.radio(
        "Metrik heatmap",
        options=[
            "avg_passthrough_pct",
            "avg_late_night_pct",
            "n_accounts",
        ],
        format_func=lambda x: {
            "avg_passthrough_pct": "Rata-rata Passthrough Velocity (%)",
            "avg_late_night_pct": "Rata-rata Late-Night Transaction Ratio (%)",
            "n_accounts": "Jumlah Rekening",
        }[x],
        horizontal=True,
    )

    pivot = channel_kyc_agg.pivot(
        index="kyc_verification_status",
        columns="primary_transaction_channel",
        values=metric_choice,
    )
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(
        pivot,
        annot=True,
        fmt="d" if metric_choice == "n_accounts" else ".2f",
        cmap="Reds" if metric_choice != "n_accounts" else "Blues",
        linewidths=0.5,
        ax=ax,
    )
    ax.set_title("Kanal Transaksi x Status KYC — Rekening Terindikasi Judi Online")
    ax.set_xlabel("Kanal Transaksi Utama")
    ax.set_ylabel("Status Verifikasi KYC")
    st.pyplot(fig)
    plt.close(fig)

    st.dataframe(
        channel_kyc_agg.sort_values(metric_choice, ascending=False)
        .round(3)
        .reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )
    st.info(
        "Passthrough velocity seragam tinggi (~97%) di semua kombinasi; "
        "pembeda prioritas adalah late-night ratio (tertinggi pada BI-FAST dengan "
        "KYC lemah) dan jumlah rekening (terbesar pada QRIS x rekening jual-beli)."
    )

with tab2:
    st.subheader("Jenis institusi dengan eksposur risiko tertinggi")

    institution_analysis = (
        df_filtered.groupby("institution_type", observed=True)
        .agg(total_accounts=("account_id", "count"))
        .join(
            high_risk_df.groupby("institution_type", observed=True).agg(
                high_risk_accounts=("account_id", "count"),
                avg_aml_risk_score=("aml_composite_risk_score", "mean"),
            )
        )
        .fillna(0)
    )
    institution_analysis["high_risk_pct"] = (
        institution_analysis["high_risk_accounts"]
        / institution_analysis["total_accounts"]
        * 100
    )
    institution_analysis = institution_analysis.sort_values(
        "high_risk_pct", ascending=False
    )

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    sns.barplot(
        data=institution_analysis.reset_index(),
        x="high_risk_pct",
        y="institution_type",
        hue="institution_type",
        palette="Reds_r",
        legend=False,
        ax=axes[0],
    )
    axes[0].set_title("Proporsi Rekening Berisiko per Institusi (%)")
    axes[0].set_xlabel("Proporsi (%)")
    axes[0].set_ylabel("")
    sns.barplot(
        data=institution_analysis.reset_index(),
        x="avg_aml_risk_score",
        y="institution_type",
        hue="institution_type",
        palette="Oranges_r",
        legend=False,
        ax=axes[1],
    )
    axes[1].set_title("Rata-rata AML Composite Risk Score (Rekening Berisiko)")
    axes[1].set_xlabel("Skor rata-rata")
    axes[1].set_ylabel("")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.dataframe(
        institution_analysis.round(2).reset_index(),
        use_container_width=True,
        hide_index=True,
    )
    st.info(
        "Digital Neo-Bank dan penyedia e-wallet memiliki proporsi rekening "
        "berisiko tertinggi (~33%); pembeda utama adalah jumlah/proporsi, "
        "bukan skor AML rata-rata yang relatif setara antar institusi."
    )

with tab3:
    st.subheader("Indikator anomali utama paling dominan")

    anomaly_analysis = (
        high_risk_df.groupby("primary_anomaly_indicator", observed=True)
        .agg(
            n_accounts=("account_id", "count"),
            avg_late_night_pct=("late_night_transaction_ratio", "mean"),
            avg_passthrough_pct=("passthrough_velocity_pct", "mean"),
            avg_aml_risk_score=("aml_composite_risk_score", "mean"),
        )
        .sort_values("n_accounts", ascending=False)
    )
    anomaly_analysis["share_pct"] = (
        anomaly_analysis["n_accounts"] / len(high_risk_df) * 100
    )

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(
        data=anomaly_analysis.reset_index(),
        x="n_accounts",
        y="primary_anomaly_indicator",
        hue="primary_anomaly_indicator",
        palette="viridis",
        legend=False,
        ax=ax,
    )
    ax.set_title("Indikator Anomali Utama pada Rekening Terindikasi Judi Online")
    ax.set_xlabel("Jumlah rekening")
    ax.set_ylabel("")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.dataframe(
        anomaly_analysis.round(2).reset_index(),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("**Komposisi klasifikasi risiko per indikator anomali**")
    crosstab = pd.crosstab(
        high_risk_df["primary_anomaly_indicator"],
        high_risk_df["account_risk_classification"],
    )
    fig, ax = plt.subplots(figsize=(12, 5))
    crosstab.plot(kind="barh", stacked=True, colormap="Set2", edgecolor="white", ax=ax)
    ax.set_title("Komposisi Klasifikasi Risiko per Indikator Anomali")
    ax.set_xlabel("Jumlah rekening")
    ax.set_ylabel("")
    ax.legend(title="Klasifikasi Risiko", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.info(
        "Dormant-Sudden-High-Volume dan VPN-Proxy-Multi-Device-Churn mendominasi "
        "(~95% rekening berisiko); kasus VPN-Proxy eksklusif pada klasifikasi "
        "Dormant-Takeover-Syndicate."
    )

with tab4:
    st.subheader("Kalibrasi ambang skor risiko AML untuk auto-flag")

    mule_mask = df_filtered["account_risk_classification"].isin(selected_risk)
    n_mule = int(mule_mask.sum())
    n_non_mule = int((~mule_mask).sum())

    if n_mule == 0 or n_non_mule == 0:
        st.info("Filter saat ini tidak menyisakan dua kelompok (terindikasi vs tidak) untuk kalibrasi ambang.")
    else:
        thr_rows = []
        for t in range(20, 95, 5):
            flagged = df_filtered["aml_composite_risk_score"] >= t
            capture = df_filtered.loc[flagged & mule_mask].shape[0] / n_mule * 100
            false_positive = df_filtered.loc[flagged & ~mule_mask].shape[0] / n_non_mule * 100
            thr_rows.append((t, int(flagged.sum()), capture, false_positive))
        thr_df = pd.DataFrame(
            thr_rows,
            columns=["ambang_skor", "n_tertandai", "capture_terindikasi_pct", "salah_tandai_pct"],
        )

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(thr_df["ambang_skor"], thr_df["capture_terindikasi_pct"],
                marker="o", color="crimson", label="Capture rate terindikasi (%)")
        ax.plot(thr_df["ambang_skor"], thr_df["salah_tandai_pct"],
                marker="s", color="steelblue", label="Salah-tandai akun lain (%)")
        ax.axvline(50, color="green", linestyle="--", label="Rekomendasi ambang >= 50")
        ax.set_title("Kalibrasi Ambang aml_composite_risk_score")
        ax.set_xlabel("Ambang skor AML")
        ax.set_ylabel("Persentase (%)")
        ax.legend()
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.dataframe(thr_df.round(2), use_container_width=True, hide_index=True)
        st.info(
            "Pada data penuh, ambang >= 50 menangkap ~97% rekening terindikasi dengan "
            "~0% akun lain tertandai; ambang >= 45 menangkap ~99,6% dengan salah-tandai 0,13%."
        )

with tab5:
    st.subheader("Profil usia: rekening terindikasi vs tidak terindikasi")

    age_df = df_filtered.copy()
    age_df["kelompok_usia"] = pd.cut(
        age_df["account_holder_age"],
        bins=[16, 24, 34, 44, 54, 70],
        labels=["<25", "25-34", "35-44", "45-54", ">=55"],
    )
    age_df["terindikasi"] = age_df["account_risk_classification"].isin(selected_risk)
    age_tab = (
        age_df.groupby("kelompok_usia", observed=True)
        .agg(total_rekening=("terindikasi", "size"), terindikasi=("terindikasi", "sum"))
    )
    age_tab["tidak_terindikasi"] = age_tab["total_rekening"] - age_tab["terindikasi"]
    age_tab["pct_terindikasi"] = age_tab["terindikasi"] / age_tab["total_rekening"] * 100
    age_tab["pct_tidak"] = 100 - age_tab["pct_terindikasi"]

    fig, ax = plt.subplots(figsize=(10, 5))
    y = np.arange(len(age_tab))
    ax.barh(y, age_tab["terindikasi"], color="crimson", label="Terindikasi judi online")
    ax.barh(y, age_tab["tidak_terindikasi"], left=age_tab["terindikasi"],
            color="lightgray", label="Tidak terindikasi")
    for i, row in enumerate(age_tab.itertuples()):
        ax.text(row.terindikasi / 2, i, f"{row.terindikasi:,}",
                ha="center", va="center", color="white", fontweight="bold")
        ax.text(row.terindikasi + row.tidak_terindikasi / 2, i, f"{row.tidak_terindikasi:,}",
                ha="center", va="center")
        ax.text(row.total_rekening + 40, i, f"{row.pct_terindikasi:.1f}%",
                va="center", fontweight="bold", color="crimson")
    ax.set_yticks(y, age_tab.index)
    ax.invert_yaxis()
    ax.set_xlabel("Jumlah rekening")
    ax.set_title("Rekening Terindikasi vs Tidak Terindikasi per Kelompok Usia")
    ax.legend(loc="lower right")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.dataframe(age_tab.round(2).reset_index(), use_container_width=True, hide_index=True)
    st.info(
        "Dua kelompok usia paling ujung paling rentan: >=55 tahun (62,5%) dan <25 tahun "
        "(40,6%); kelompok 35-44 tidak memiliki rekening terindikasi sama sekali."
    )

with tab6:
    st.subheader("Sinyal perangkat sebagai auto-flag kedua")

    dev_tab = (
        df_filtered.groupby("account_risk_classification")
        [["device_fingerprint_change_count", "device_churn_rate"]]
        .mean()
        .reset_index()
        .sort_values("device_fingerprint_change_count")
    )

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    sns.barplot(data=dev_tab, x="device_fingerprint_change_count",
                y="account_risk_classification", hue="account_risk_classification",
                palette="magma", legend=False, ax=axes[0])
    axes[0].axvline(5, color="red", linestyle="--")
    axes[0].set_title("Rata-rata Pergantian Fingerprint Perangkat")
    axes[0].set_xlabel("device_fingerprint_change_count")
    axes[0].set_ylabel("")
    sns.barplot(data=dev_tab, x="device_churn_rate",
                y="account_risk_classification", hue="account_risk_classification",
                palette="viridis", legend=False, ax=axes[1])
    axes[1].set_title("Rata-rata Device Churn Rate")
    axes[1].set_xlabel("device_churn_rate")
    axes[1].set_ylabel("")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.dataframe(dev_tab.round(3), use_container_width=True, hide_index=True)
    st.info(
        "Pada data penuh, ambang >= 5 kali pergantian fingerprint menangkap 100% "
        "rekening terindikasi dengan 0% akun lain tertandai."
    )

with tab7:
    st.subheader("Durasi dana & frekuensi micro-deposit")

    hold_tab = (
        df_filtered.groupby("account_risk_classification")
        [["average_holding_duration_hours", "micro_deposit_frequency_ratio"]]
        .mean()
        .reset_index()
        .sort_values("average_holding_duration_hours")
    )

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    sns.barplot(data=hold_tab, x="average_holding_duration_hours",
                y="account_risk_classification", hue="account_risk_classification",
                palette="coolwarm", legend=False, ax=axes[0])
    axes[0].set_xscale("log")
    axes[0].set_title("Rata-rata Durasi Dana Menginap (jam, skala log)")
    axes[0].set_xlabel("average_holding_duration_hours (log)")
    axes[0].set_ylabel("")
    sns.barplot(data=hold_tab, x="micro_deposit_frequency_ratio",
                y="account_risk_classification", hue="account_risk_classification",
                palette="flare", legend=False, ax=axes[1])
    axes[1].set_title("Rata-rata Micro-Deposit Frequency Ratio")
    axes[1].set_xlabel("micro_deposit_frequency_ratio")
    axes[1].set_ylabel("")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.dataframe(hold_tab.round(3), use_container_width=True, hide_index=True)
    st.info(
        "Rekening terindikasi menahan dana < 1 jam dengan rasio micro-deposit 9-15, "
        "dibanding ~85 jam dan rasio ~1 pada akun tidak terindikasi."
    )


st.markdown("---")
st.caption(
    "Program Komputer — Alif Setyo Wisnuaji | Matematika S1, "
    "Fakultas Sains dan Matematika, Universitas Diponegoro"
)
