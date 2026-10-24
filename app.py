"""
DATASPHERE — ENTERPRISE ANALYTICS DASHBOARD v2.0
World-Class Professional UI with AI Insights, Chart Builder, Tab Navigation
Includes: Landing Page, Login, Register, SQLite3 Auth
"""

import base64
import io
import os
import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats

import dash
from dash import dcc, html, Input, Output, State, callback_context, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from flask import Flask, render_template, request, redirect, url_for, session, flash
import auth as auth_module

# ===============================
# APP SETUP
# ===============================
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True,
    url_base_pathname='/dashboard/'
)
app.title = "DataSphere | Enterprise Analytics Platform v2.0"
server = app.server  # Flask server instance

# ===============================
# FLASK CONFIGURATION
# ===============================
server.secret_key = os.environ.get('SECRET_KEY', 'datasphere_secret_key_2024_enterprise')
server.template_folder = os.path.join(os.path.dirname(__file__), 'templates')

# ===============================
# AUTH MIDDLEWARE — Protect /dashboard/
# ===============================
@server.before_request
def require_login():
    """Redirect unauthenticated users away from /dashboard/"""
    public_paths = ['/', '/login', '/register', '/logout', '/favicon.ico']
    path = request.path

    # Allow public paths and static assets
    if path in public_paths or path.startswith('/static') or path.startswith('/_dash'):
        return None

    # Protect dashboard
    if path.startswith('/dashboard') and 'user_id' not in session:
        flash('Please sign in to access the dashboard.', 'error')
        return redirect(url_for('login'))

    return None

# ===============================
# FLASK ROUTES — Landing, Login, Register
# ===============================

@server.route('/')
def landing():
    """Landing page."""
    return render_template('landing.html')


@server.route('/login', methods=['GET', 'POST'])
def login():
    """Login page — GET renders form, POST authenticates."""
    # Already logged in → go to dashboard
    if 'user_id' in session:
        return redirect('/dashboard/')

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password   = request.form.get('password', '')

        if not identifier or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('login.html')

        ip = request.remote_addr
        success, message, user_data = auth_module.login_user(identifier, password, ip)

        if success:
            session['user_id']   = user_data['id']
            session['username']  = user_data['username']
            session['full_name'] = user_data['full_name']
            session['email']     = user_data['email']
            flash(f"Welcome back, {user_data['full_name']}! 🎉", 'success')
            return redirect('/dashboard/')
        else:
            flash(message, 'error')
            return render_template('login.html')

    return render_template('login.html')


@server.route('/register', methods=['GET', 'POST'])
def register():
    """Register page — GET renders form, POST creates account."""
    if 'user_id' in session:
        return redirect('/dashboard/')

    if request.method == 'POST':
        full_name        = request.form.get('full_name', '').strip()
        username         = request.form.get('username', '').strip()
        email            = request.form.get('email', '').strip()
        password         = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        terms            = request.form.get('terms')

        # Validation
        if not terms:
            flash('You must agree to the Terms of Service.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return render_template('register.html')

        success, message = auth_module.register_user(full_name, username, email, password)

        if success:
            flash(message, 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')
            return render_template('register.html')

    return render_template('register.html')


@server.route('/logout')
def logout():
    """Clear session and redirect to landing."""
    name = session.get('full_name', 'User')
    session.clear()
    flash(f'You have been signed out. See you soon, {name}!', 'success')
    return redirect('/')

# ===============================
# PROFESSIONAL INDEX STRING — FULL CSS
# ===============================
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
        <style>
            /* ============================================================
               ROOT DESIGN TOKENS
            ============================================================ */
            :root {
                --bg:           #0d1117;
                --surface:      #161b22;
                --surface-2:    #21262d;
                --surface-3:    #2d333b;
                --primary:      #58a6ff;
                --primary-glow: rgba(88,166,255,0.15);
                --primary-dim:  rgba(88,166,255,0.08);
                --secondary:    #7ee787;
                --warning:      #e3b341;
                --danger:       #f85149;
                --info:         #79c0ff;
                --purple:       #d2a8ff;
                --border:       #30363d;
                --border-focus: rgba(88,166,255,0.6);
                --text-1:       #e6edf3;
                --text-2:       #8b949e;
                --text-3:       #484f58;
                --gradient-brand: linear-gradient(135deg, #58a6ff 0%, #79c0ff 50%, #d2a8ff 100%);
                --gradient-green: linear-gradient(135deg, #7ee787 0%, #3fb950 100%);
                --gradient-amber: linear-gradient(135deg, #e3b341 0%, #d29922 100%);
                --gradient-red:   linear-gradient(135deg, #f85149 0%, #da3633 100%);
                --gradient-purple: linear-gradient(135deg, #d2a8ff 0%, #a371f7 100%);
                --shadow-sm:    0 1px 3px rgba(0,0,0,0.4);
                --shadow-md:    0 4px 12px rgba(0,0,0,0.5);
                --shadow-lg:    0 8px 24px rgba(0,0,0,0.6);
                --shadow-xl:    0 16px 48px rgba(0,0,0,0.7);
                --shadow-glow:  0 0 24px rgba(88,166,255,0.3);
                --radius-sm:    6px;
                --radius-md:    10px;
                --radius-lg:    16px;
                --radius-xl:    24px;
                --transition:   all 0.25s cubic-bezier(0.4,0,0.2,1);
            }

            /* ============================================================
               RESET & BASE
            ============================================================ */
            *, *::before, *::after {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            html {
                scroll-behavior: smooth;
                font-size: 16px;
            }

            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background-color: var(--bg);
                background-image:
                    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(88,166,255,0.06) 0%, transparent 100%);
                color: var(--text-1);
                line-height: 1.6;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
                min-height: 100vh;
            }

            /* ============================================================
               SCROLLBAR
            ============================================================ */
            ::-webkit-scrollbar { width: 6px; height: 6px; }
            ::-webkit-scrollbar-track { background: var(--bg); }
            ::-webkit-scrollbar-thumb {
                background: var(--surface-3);
                border-radius: 3px;
            }
            ::-webkit-scrollbar-thumb:hover { background: var(--primary); }

            /* ============================================================
               ANIMATIONS
            ============================================================ */
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(24px); }
                to   { opacity: 1; transform: translateY(0); }
            }

            @keyframes slideInLeft {
                from { opacity: 0; transform: translateX(-24px); }
                to   { opacity: 1; transform: translateX(0); }
            }

            @keyframes pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50%       { opacity: 0.75; transform: scale(1.06); }
            }

            @keyframes shimmer {
                0%   { background-position: -1200px 0; }
                100% { background-position:  1200px 0; }
            }

            @keyframes glow-pulse {
                0%, 100% { box-shadow: 0 0 12px rgba(88,166,255,0.2); }
                50%       { box-shadow: 0 0 32px rgba(88,166,255,0.5); }
            }

            @keyframes status-blink {
                0%, 100% { opacity: 1; }
                50%       { opacity: 0.4; }
            }

            @keyframes border-rotate {
                0%   { background-position: 0% 50%; }
                50%  { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50%       { transform: translateY(-8px); }
            }

            @keyframes spin-slow {
                from { transform: rotate(0deg); }
                to   { transform: rotate(360deg); }
            }

            .animate-in        { animation: fadeInUp 0.55s ease-out both; }
            .animate-slide-left{ animation: slideInLeft 0.55s ease-out both; }
            .animate-delay-1   { animation-delay: 0.1s; }
            .animate-delay-2   { animation-delay: 0.2s; }
            .animate-delay-3   { animation-delay: 0.3s; }
            .animate-delay-4   { animation-delay: 0.4s; }

            /* ============================================================
               NAVBAR
            ============================================================ */
            .ds-navbar {
                position: sticky;
                top: 0;
                z-index: 9999;
                background: rgba(13,17,23,0.85);
                backdrop-filter: blur(20px) saturate(180%);
                -webkit-backdrop-filter: blur(20px) saturate(180%);
                border-bottom: 1px solid var(--border);
                padding: 0 2rem;
                height: 64px;
                display: flex;
                align-items: center;
                box-shadow: 0 1px 0 rgba(88,166,255,0.08), var(--shadow-sm);
            }

            .ds-navbar::after {
                content: '';
                position: absolute;
                bottom: -1px;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(90deg,
                    transparent 0%,
                    rgba(88,166,255,0.4) 30%,
                    rgba(210,168,255,0.4) 70%,
                    transparent 100%);
            }

            .ds-navbar-inner {
                display: flex;
                align-items: center;
                justify-content: space-between;
                width: 100%;
                max-width: 1600px;
                margin: 0 auto;
            }

            .ds-brand {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                text-decoration: none;
            }

            .ds-brand-icon {
                width: 36px;
                height: 36px;
                border-radius: var(--radius-sm);
                background: var(--gradient-brand);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #0d1117;
                font-size: 1.1rem;
                box-shadow: 0 0 16px rgba(88,166,255,0.4);
                flex-shrink: 0;
            }

            .ds-brand-name {
                font-size: 1.25rem;
                font-weight: 800;
                background: var(--gradient-brand);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                letter-spacing: -0.02em;
            }

            .ds-version-badge {
                font-size: 0.65rem;
                font-weight: 700;
                padding: 2px 8px;
                border-radius: 999px;
                background: var(--primary-dim);
                color: var(--primary);
                border: 1px solid rgba(88,166,255,0.3);
                letter-spacing: 0.05em;
                text-transform: uppercase;
            }

            .ds-navbar-center {
                display: flex;
                align-items: center;
                gap: 1rem;
            }

            .ds-live-badge {
                display: flex;
                align-items: center;
                gap: 0.4rem;
                font-size: 0.75rem;
                font-weight: 600;
                color: var(--secondary);
                padding: 4px 10px;
                border-radius: 999px;
                background: rgba(126,231,135,0.08);
                border: 1px solid rgba(126,231,135,0.25);
            }

            .ds-status-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: var(--secondary);
                animation: status-blink 2s ease-in-out infinite;
                box-shadow: 0 0 6px var(--secondary);
                flex-shrink: 0;
            }

            .ds-data-loaded-badge {
                display: none;
                align-items: center;
                gap: 0.4rem;
                font-size: 0.75rem;
                font-weight: 600;
                color: var(--primary);
                padding: 4px 10px;
                border-radius: 999px;
                background: var(--primary-dim);
                border: 1px solid rgba(88,166,255,0.3);
            }

            .ds-data-loaded-badge.visible {
                display: flex;
            }

            .ds-navbar-right {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .ds-datetime {
                font-size: 0.8rem;
                color: var(--text-2);
                font-weight: 500;
                padding: 0 0.75rem;
                border-left: 1px solid var(--border);
                margin-left: 0.25rem;
            }

            /* Navbar Buttons */
            .ds-btn {
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                padding: 6px 14px;
                border-radius: var(--radius-sm);
                font-size: 0.8rem;
                font-weight: 600;
                cursor: pointer;
                border: 1px solid transparent;
                transition: var(--transition);
                white-space: nowrap;
                font-family: 'Inter', sans-serif;
            }

            .ds-btn-primary {
                background: var(--primary-glow);
                color: var(--primary);
                border-color: rgba(88,166,255,0.3);
            }

            .ds-btn-primary:hover {
                background: rgba(88,166,255,0.25);
                border-color: var(--primary);
                box-shadow: 0 0 16px rgba(88,166,255,0.2);
                color: var(--primary);
            }

            .ds-btn-ghost {
                background: transparent;
                color: var(--text-2);
                border-color: var(--border);
            }

            .ds-btn-ghost:hover {
                background: var(--surface-2);
                color: var(--text-1);
                border-color: rgba(88,166,255,0.4);
            }

            .ds-btn-icon {
                padding: 6px 10px;
                background: transparent;
                color: var(--text-2);
                border-color: var(--border);
            }

            .ds-btn-icon:hover {
                background: var(--surface-2);
                color: var(--text-1);
                border-color: rgba(88,166,255,0.4);
            }

            /* ============================================================
               HERO / UPLOAD SECTION
            ============================================================ */
            .ds-hero {
                min-height: calc(100vh - 64px);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 4rem 2rem;
                position: relative;
                overflow: hidden;
            }

            /* Animated grid background */
            .ds-hero::before {
                content: '';
                position: absolute;
                inset: 0;
                background-image:
                    linear-gradient(rgba(88,166,255,0.04) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(88,166,255,0.04) 1px, transparent 1px);
                background-size: 60px 60px;
                mask-image: radial-gradient(ellipse 80% 70% at 50% 50%, black 30%, transparent 100%);
                -webkit-mask-image: radial-gradient(ellipse 80% 70% at 50% 50%, black 30%, transparent 100%);
            }

            /* Glow orbs */
            .ds-hero::after {
                content: '';
                position: absolute;
                top: 20%;
                left: 50%;
                transform: translateX(-50%);
                width: 600px;
                height: 300px;
                background: radial-gradient(ellipse, rgba(88,166,255,0.06) 0%, transparent 70%);
                pointer-events: none;
            }

            .ds-hero-content {
                position: relative;
                z-index: 1;
                text-align: center;
                max-width: 700px;
                width: 100%;
            }

            .ds-hero-eyebrow {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 6px 16px;
                border-radius: 999px;
                background: var(--primary-dim);
                border: 1px solid rgba(88,166,255,0.25);
                color: var(--primary);
                font-size: 0.8rem;
                font-weight: 600;
                margin-bottom: 1.5rem;
                letter-spacing: 0.05em;
                text-transform: uppercase;
            }

            .ds-hero-title {
                font-size: clamp(2rem, 5vw, 3.25rem);
                font-weight: 900;
                letter-spacing: -0.03em;
                line-height: 1.1;
                margin-bottom: 1rem;
                background: var(--gradient-brand);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .ds-hero-subtitle {
                font-size: 1.05rem;
                color: var(--text-2);
                margin-bottom: 3rem;
                line-height: 1.7;
            }

            /* Upload Zone */
            .ds-upload-zone {
                width: 100%;
                background: linear-gradient(135deg,
                    rgba(22,27,34,0.9) 0%,
                    rgba(33,38,45,0.9) 100%);
                border: 2px dashed var(--border);
                border-radius: var(--radius-xl);
                padding: 3.5rem 2rem;
                cursor: pointer;
                position: relative;
                overflow: hidden;
                transition: var(--transition);
                backdrop-filter: blur(10px);
            }

            .ds-upload-zone::before {
                content: '';
                position: absolute;
                inset: 0;
                background: linear-gradient(135deg,
                    rgba(88,166,255,0.03) 0%,
                    rgba(210,168,255,0.03) 100%);
                opacity: 0;
                transition: opacity 0.4s ease;
            }

            .ds-upload-zone:hover {
                border-color: var(--primary);
                transform: translateY(-4px);
                box-shadow: 0 0 0 1px rgba(88,166,255,0.2), var(--shadow-glow);
            }

            .ds-upload-zone:hover::before {
                opacity: 1;
            }

            .ds-upload-icon-wrap {
                width: 88px;
                height: 88px;
                border-radius: 50%;
                background: linear-gradient(135deg, rgba(88,166,255,0.12), rgba(210,168,255,0.08));
                border: 1px solid rgba(88,166,255,0.2);
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1.5rem;
                font-size: 2.25rem;
                color: var(--primary);
                animation: float 3s ease-in-out infinite;
                position: relative;
                z-index: 1;
            }

            .ds-upload-title {
                font-size: 1.25rem;
                font-weight: 700;
                color: var(--text-1);
                margin-bottom: 0.4rem;
                position: relative;
                z-index: 1;
            }

            .ds-upload-subtitle {
                font-size: 0.875rem;
                color: var(--text-2);
                position: relative;
                z-index: 1;
            }

            .ds-format-pills {
                display: flex;
                justify-content: center;
                gap: 0.5rem;
                flex-wrap: wrap;
                margin-top: 1.5rem;
                position: relative;
                z-index: 1;
            }

            .ds-format-pill {
                display: inline-flex;
                align-items: center;
                gap: 0.3rem;
                padding: 4px 12px;
                border-radius: 999px;
                font-size: 0.75rem;
                font-weight: 600;
                border: 1px solid var(--border);
                color: var(--text-2);
                background: var(--surface);
            }

            .ds-quick-load {
                margin-top: 2.5rem;
                text-align: center;
            }

            .ds-quick-load-label {
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: var(--text-3);
                font-weight: 600;
                margin-bottom: 0.75rem;
            }

            .ds-sample-chips {
                display: flex;
                justify-content: center;
                gap: 0.5rem;
                flex-wrap: wrap;
            }

            .ds-sample-chip {
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                padding: 6px 14px;
                border-radius: 999px;
                font-size: 0.8rem;
                font-weight: 500;
                background: var(--surface-2);
                border: 1px solid var(--border);
                color: var(--text-2);
                cursor: default;
                transition: var(--transition);
            }

            .ds-sample-chip:hover {
                border-color: rgba(88,166,255,0.4);
                color: var(--primary);
                background: var(--primary-dim);
            }

            /* ============================================================
               DATASET INFO BANNER
            ============================================================ */
            .ds-info-banner {
                display: flex;
                align-items: center;
                gap: 1.5rem;
                padding: 0.875rem 1.5rem;
                background: linear-gradient(135deg,
                    rgba(22,27,34,0.95) 0%,
                    rgba(33,38,45,0.95) 100%);
                border: 1px solid var(--border);
                border-left: 3px solid var(--primary);
                border-radius: var(--radius-md);
                backdrop-filter: blur(8px);
                flex-wrap: wrap;
                gap: 1rem;
            }

            .ds-info-banner-item {
                display: flex;
                flex-direction: column;
                gap: 1px;
            }

            .ds-info-banner-label {
                font-size: 0.65rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: var(--text-3);
                font-weight: 700;
            }

            .ds-info-banner-value {
                font-size: 0.9rem;
                font-weight: 700;
                color: var(--text-1);
            }

            .ds-info-sep {
                width: 1px;
                height: 28px;
                background: var(--border);
                flex-shrink: 0;
            }

            /* ============================================================
               TAB NAVIGATION
            ============================================================ */
            .ds-tabs-wrapper {
                margin: 1.5rem 0 0;
            }

            .nav-tabs {
                border-bottom: 1px solid var(--border) !important;
                gap: 0.25rem;
                flex-wrap: nowrap;
                overflow-x: auto;
                padding-bottom: 0;
            }

            .nav-tabs .nav-link {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.7rem 1.25rem !important;
                border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
                font-size: 0.875rem !important;
                font-weight: 600 !important;
                color: var(--text-2) !important;
                border: 1px solid transparent !important;
                border-bottom: none !important;
                background: transparent !important;
                transition: var(--transition) !important;
                white-space: nowrap;
                cursor: pointer;
            }

            .nav-tabs .nav-link:hover {
                color: var(--text-1) !important;
                background: var(--surface-2) !important;
                border-color: var(--border) !important;
                border-bottom-color: transparent !important;
            }

            .nav-tabs .nav-link.active {
                color: var(--primary) !important;
                background: var(--surface) !important;
                border-color: var(--border) !important;
                border-bottom-color: var(--surface) !important;
                box-shadow: 0 0 12px rgba(88,166,255,0.1);
            }

            .tab-content {
                background: transparent !important;
                padding-top: 1.5rem;
            }

            /* ============================================================
               SECTION TITLE
            ============================================================ */
            .ds-section-title {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 1.25rem;
            }

            .ds-section-title-bar {
                width: 4px;
                height: 24px;
                border-radius: 2px;
                background: var(--gradient-brand);
                flex-shrink: 0;
                box-shadow: 0 0 8px rgba(88,166,255,0.4);
            }

            .ds-section-title-text {
                font-size: 1.05rem;
                font-weight: 700;
                color: var(--text-1);
            }

            .ds-section-title-badge {
                margin-left: auto;
                font-size: 0.7rem;
                font-weight: 600;
                padding: 3px 10px;
                border-radius: 999px;
                background: var(--surface-2);
                border: 1px solid var(--border);
                color: var(--text-2);
            }

            /* ============================================================
               KPI CARDS — GLASSMORPHISM
            ============================================================ */
            .ds-kpi-card {
                position: relative;
                background: linear-gradient(135deg,
                    rgba(22,27,34,0.95) 0%,
                    rgba(33,38,45,0.85) 100%);
                border: 1px solid var(--border);
                border-radius: var(--radius-lg);
                padding: 1.5rem;
                overflow: hidden;
                transition: var(--transition);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                height: 100%;
            }

            .ds-kpi-card::before {
                content: '';
                position: absolute;
                inset: 0;
                border-radius: var(--radius-lg);
                border: 1px solid rgba(88,166,255,0);
                transition: var(--transition);
                pointer-events: none;
            }

            .ds-kpi-card:hover {
                transform: translateY(-6px);
                box-shadow: 0 12px 32px rgba(0,0,0,0.5), 0 0 0 1px rgba(88,166,255,0.2), var(--shadow-glow);
                border-color: rgba(88,166,255,0.35);
            }

            .ds-kpi-card:hover::before {
                border-color: rgba(88,166,255,0.2);
            }

            /* Corner glow */
            .ds-kpi-card-glow {
                position: absolute;
                top: -30px;
                right: -30px;
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(88,166,255,0.12) 0%, transparent 70%);
                pointer-events: none;
            }

            .ds-kpi-top {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                margin-bottom: 1rem;
            }

            .ds-kpi-icon {
                width: 40px;
                height: 40px;
                border-radius: var(--radius-sm);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.1rem;
                flex-shrink: 0;
            }

            .ds-kpi-icon-blue   { background: rgba(88,166,255,0.12);  color: var(--primary); }
            .ds-kpi-icon-green  { background: rgba(126,231,135,0.12); color: var(--secondary); }
            .ds-kpi-icon-amber  { background: rgba(227,179,65,0.12);  color: var(--warning); }
            .ds-kpi-icon-purple { background: rgba(210,168,255,0.12); color: var(--purple); }

            .ds-kpi-trend {
                display: inline-flex;
                align-items: center;
                gap: 0.25rem;
                padding: 3px 8px;
                border-radius: 999px;
                font-size: 0.7rem;
                font-weight: 700;
            }

            .ds-kpi-trend-up   { background: rgba(126,231,135,0.1); color: var(--secondary); border: 1px solid rgba(126,231,135,0.25); }
            .ds-kpi-trend-down { background: rgba(248,81,73,0.1);   color: var(--danger);    border: 1px solid rgba(248,81,73,0.25); }

            .ds-kpi-label {
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: var(--text-2);
                margin-bottom: 0.35rem;
            }

            .ds-kpi-value {
                font-size: 2rem;
                font-weight: 800;
                letter-spacing: -0.03em;
                line-height: 1;
                background: var(--gradient-brand);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 0.5rem;
            }

            /* Sparkline placeholder bar */
            .ds-kpi-sparkline {
                margin-top: 1rem;
                height: 36px;
                border-radius: var(--radius-sm);
                background: linear-gradient(90deg,
                    rgba(88,166,255,0.06) 0%,
                    rgba(88,166,255,0.15) 40%,
                    rgba(88,166,255,0.08) 70%,
                    rgba(88,166,255,0.18) 100%);
                position: relative;
                overflow: hidden;
            }

            .ds-kpi-sparkline::after {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 60%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(88,166,255,0.08), transparent);
                animation: shimmer 2.5s infinite;
            }

            /* ============================================================
               AI INSIGHTS
            ============================================================ */
            .ds-insights-panel {
                background: linear-gradient(135deg,
                    rgba(22,27,34,0.95) 0%,
                    rgba(33,38,45,0.9) 100%);
                border: 1px solid var(--border);
                border-radius: var(--radius-lg);
                padding: 1.5rem;
                backdrop-filter: blur(8px);
            }

            .ds-insight-item {
                display: flex;
                align-items: flex-start;
                gap: 1rem;
                padding: 1rem 1.1rem;
                border-radius: var(--radius-md);
                border: 1px solid var(--border);
                border-left-width: 3px;
                margin-bottom: 0.75rem;
                transition: var(--transition);
                background: rgba(13,17,23,0.4);
            }

            .ds-insight-item:last-child { margin-bottom: 0; }

            .ds-insight-item:hover {
                transform: translateX(4px);
                box-shadow: var(--shadow-sm);
                background: rgba(22,27,34,0.7);
            }

            .ds-insight-trend     { border-left-color: var(--primary); }
            .ds-insight-pattern   { border-left-color: var(--purple); }
            .ds-insight-anomaly   { border-left-color: var(--warning); }
            .ds-insight-quality   { border-left-color: var(--secondary); }
            .ds-insight-default   { border-left-color: var(--info); }

            .ds-insight-icon-wrap {
                width: 36px;
                height: 36px;
                border-radius: var(--radius-sm);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.1rem;
                flex-shrink: 0;
                background: var(--surface-2);
            }

            .ds-insight-title {
                font-size: 0.875rem;
                font-weight: 700;
                color: var(--text-1);
                margin-bottom: 0.2rem;
            }

            .ds-insight-text {
                font-size: 0.8rem;
                color: var(--text-2);
                line-height: 1.55;
            }

            /* ============================================================
               CHART CARDS
            ============================================================ */
            .ds-chart-card {
                background: linear-gradient(135deg,
                    rgba(22,27,34,0.98) 0%,
                    rgba(33,38,45,0.95) 100%);
                border: 1px solid var(--border);
                border-radius: var(--radius-lg);
                overflow: hidden;
                transition: var(--transition);
                margin-bottom: 1.25rem;
            }

            .ds-chart-card:hover {
                border-color: rgba(88,166,255,0.3);
                box-shadow: var(--shadow-lg);
                transform: translateY(-2px);
            }

            .ds-chart-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0.875rem 1.25rem;
                border-bottom: 1px solid var(--border);
                background: rgba(13,17,23,0.5);
            }

            .ds-chart-title {
                font-size: 0.875rem;
                font-weight: 700;
                color: var(--text-1);
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .ds-chart-type-badge {
                font-size: 0.65rem;
                font-weight: 700;
                padding: 2px 8px;
                border-radius: 999px;
                background: var(--primary-dim);
                color: var(--primary);
                border: 1px solid rgba(88,166,255,0.2);
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .ds-chart-body { padding: 0.5rem; }

            /* ============================================================
               STAT CARDS
            ============================================================ */
            .ds-stat-card {
                background: linear-gradient(135deg,
                    rgba(22,27,34,0.98) 0%,
                    rgba(33,38,45,0.95) 100%);
                border: 1px solid var(--border);
                border-radius: var(--radius-lg);
                padding: 1.5rem;
                text-align: center;
                transition: var(--transition);
                height: 100%;
            }

            .ds-stat-card:hover {
                border-color: rgba(88,166,255,0.3);
                transform: translateY(-3px);
                box-shadow: var(--shadow-md);
            }

            .ds-stat-icon {
                width: 48px;
                height: 48px;
                border-radius: var(--radius-md);
                background: var(--primary-dim);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.35rem;
                color: var(--primary);
                margin: 0 auto 1rem;
            }

            .ds-stat-label {
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: var(--text-2);
                font-weight: 700;
                margin-bottom: 0.35rem;
            }

            .ds-stat-value {
                font-size: 1.75rem;
                font-weight: 800;
                color: var(--text-1);
                letter-spacing: -0.02em;
            }

            /* ============================================================
               DATA TABLE WRAPPER
            ============================================================ */
            .ds-table-wrapper {
                background: var(--surface);
                border: 1px solid var(--border);
                border-radius: var(--radius-lg);
                overflow: hidden;
            }

            .ds-table-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 1rem 1.25rem;
                border-bottom: 1px solid var(--border);
                background: rgba(13,17,23,0.5);
                flex-wrap: wrap;
                gap: 0.75rem;
            }

            .ds-row-badge {
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                font-size: 0.75rem;
                font-weight: 600;
                padding: 4px 12px;
                border-radius: 999px;
                background: var(--surface-2);
                border: 1px solid var(--border);
                color: var(--text-2);
            }

            /* ============================================================
               CHART BUILDER CARD
            ============================================================ */
            .ds-builder-card {
                background: linear-gradient(135deg,
                    rgba(22,27,34,0.98) 0%,
                    rgba(33,38,45,0.95) 100%);
                border: 1px solid var(--border);
                border-radius: var(--radius-lg);
                padding: 1.5rem;
                backdrop-filter: blur(8px);
                margin-bottom: 1.5rem;
            }

            /* ============================================================
               FOOTER
            ============================================================ */
            .ds-footer {
                border-top: 1px solid var(--border);
                margin-top: 4rem;
                padding: 2.5rem 0;
                position: relative;
            }

            .ds-footer::before {
                content: '';
                position: absolute;
                top: -1px;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(90deg,
                    transparent 0%,
                    rgba(88,166,255,0.3) 30%,
                    rgba(210,168,255,0.3) 70%,
                    transparent 100%);
            }

            .ds-footer-grid {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 2rem;
                align-items: start;
            }

            .ds-footer-brand-name {
                font-size: 1.1rem;
                font-weight: 800;
                background: var(--gradient-brand);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 0.35rem;
            }

            .ds-footer-tagline {
                font-size: 0.8rem;
                color: var(--text-3);
            }

            .ds-footer-section-title {
                font-size: 0.7rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: var(--text-3);
                margin-bottom: 0.75rem;
            }

            .ds-tech-badges {
                display: flex;
                gap: 0.4rem;
                flex-wrap: wrap;
            }

            .ds-tech-badge {
                font-size: 0.7rem;
                font-weight: 600;
                padding: 3px 10px;
                border-radius: 999px;
                background: var(--surface-2);
                border: 1px solid var(--border);
                color: var(--text-2);
            }

            /* ============================================================
               LOADING SKELETON
            ============================================================ */
            .ds-skeleton {
                background: linear-gradient(90deg,
                    var(--surface) 25%,
                    var(--surface-2) 50%,
                    var(--surface) 75%);
                background-size: 200% 100%;
                animation: shimmer 1.5s infinite;
                border-radius: var(--radius-sm);
            }

            /* ============================================================
               TOAST
            ============================================================ */
            .toast {
                position: fixed;
                top: 80px;
                right: 20px;
                z-index: 99999;
                min-width: 320px;
                animation: slideInLeft 0.3s ease-out;
            }

            /* ============================================================
               RESPONSIVE
            ============================================================ */
            @media (max-width: 992px) {
                .ds-footer-grid { grid-template-columns: 1fr; }
                .ds-navbar-center { display: none; }
            }

            @media (max-width: 768px) {
                .container-fluid { padding: 0 0.85rem !important; }
                .ds-hero { padding: 2rem 1rem 1.5rem; min-height: auto; }
                .ds-hero-title { font-size: 1.65rem; }
                .ds-hero-subtitle { font-size: 0.88rem; margin-bottom: 1.25rem; }
                .ds-upload-zone { padding: 2rem 1rem !important; }
                .ds-upload-icon-wrap { width: 60px !important; height: 60px !important; font-size: 1.6rem !important; margin-bottom: 1rem !important; }
                .ds-upload-title { font-size: 1.1rem !important; }
                .ds-kpi-value { font-size: 1.45rem; }
                .ds-navbar { padding: 0 0.85rem; }
                .ds-datetime { display: none; }
                .ds-btn span { display: none; }
                #settings-btn, #help-btn { display: none; }
                .nav-tabs { flex-wrap: nowrap !important; overflow-x: auto !important; overflow-y: hidden !important; -webkit-overflow-scrolling: touch !important; padding-bottom: 2px !important; }
                .nav-tabs .nav-link { white-space: nowrap !important; font-size: 0.82rem !important; padding: 0.45rem 0.75rem !important; }
                .chart-container { padding: 1rem 0.65rem !important; }
                .ds-info-banner { gap: 0.75rem !important; padding: 0.75rem 1rem !important; }
                .ds-info-banner-item { min-width: 45%; }
            }

            @media (max-width: 480px) {
                .container-fluid { padding: 0 0.5rem !important; }
                .ds-navbar { height: 56px; }
                .ds-brand-name { font-size: 1.05rem; }
                .ds-version-badge { display: none; }
                .ds-btn { padding: 5px 8px; }
                .ds-kpi-card { padding: 1rem; }
                .ds-kpi-value { font-size: 1.3rem; }
                .ds-info-banner-item { min-width: 100%; }
                .toast { min-width: 280px; right: 10px; top: 65px; }
            }

            /* ============================================================
               MISC OVERRIDES
            ============================================================ */
            .container-fluid { max-width: 1600px; margin: 0 auto; padding: 0 1.5rem; }

            /* Bootstrap override — dark dropdowns */
            .dropdown-menu {
                background: var(--surface-2) !important;
                border-color: var(--border) !important;
            }
            .dropdown-item { color: var(--text-1) !important; }
            .dropdown-item:hover { background: var(--surface-3) !important; }

            /* dcc.Loading spinner override */
            ._dash-loading { background: transparent !important; }

            /* Alert styling */
            .alert { border-radius: var(--radius-md) !important; }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ===============================
# HELPER FUNCTIONS  (preserved exactly)
# ===============================

def parse_contents(contents, filename):
    """Parse uploaded file contents"""
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if filename.endswith(".csv"):
            return pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif filename.endswith((".xlsx", ".xls")):
            return pd.read_excel(io.BytesIO(decoded))
        else:
            return None
    except Exception as e:
        print(f"Error parsing file: {e}")
        return None

def detect_column_types(df):
    """Detect numeric, categorical, and datetime columns"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

    # Try to convert string columns to datetime
    for col in categorical_cols[:]:
        try:
            pd.to_datetime(df[col], format='mixed', errors='coerce')
            datetime_cols.append(col)
            categorical_cols.remove(col)
        except:
            pass

    return numeric_cols, categorical_cols, datetime_cols

def generate_ai_insights(df, numeric_cols, categorical_cols, datetime_cols):
    """Generate AI-powered insights from the data"""
    insights = []

    try:
        # 1. Trend Analysis
        if numeric_cols and len(df) > 1:
            col = numeric_cols[0]
            values = df[col].dropna()
            if len(values) >= 2:
                trend = ((values.iloc[-1] - values.iloc[0]) / values.iloc[0] * 100)
                if abs(trend) > 5:
                    direction = "increased" if trend > 0 else "decreased"
                    strength = "significantly" if abs(trend) > 20 else "moderately"
                    insights.append({
                        "icon": "📈" if trend > 0 else "📉",
                        "title": "Trend Detected",
                        "text": f"{col} has {strength} {direction} by {abs(trend):.1f}% from start to end of dataset",
                        "type": "trend"
                    })

        # 2. Pattern Discovery (Day of Week)
        if datetime_cols and numeric_cols:
            try:
                df_copy = df.copy()
                date_col = datetime_cols[0]
                num_col = numeric_cols[0]
                df_copy[date_col] = pd.to_datetime(df_copy[date_col], format='mixed', errors='coerce')
                df_copy['day_name'] = df_copy[date_col].dt.day_name()

                day_avg = df_copy.groupby('day_name')[num_col].mean()
                if len(day_avg) > 0:
                    best_day = day_avg.idxmax()
                    best_value = day_avg.max()
                    worst_day = day_avg.idxmin()
                    insights.append({
                        "icon": "📅",
                        "title": "Pattern Discovered",
                        "text": f"Peak activity occurs on {best_day} with average of {best_value:,.2f}. Lowest on {worst_day}.",
                        "type": "pattern"
                    })
            except:
                pass

        # 3. Outlier Detection
        if numeric_cols:
            col = numeric_cols[0]
            values = df[col].dropna()
            if len(values) > 3:
                z_scores = np.abs(stats.zscore(values))
                outliers = len(z_scores[z_scores > 3])
                if outliers > 0:
                    pct = (outliers / len(values)) * 100
                    insights.append({
                        "icon": "⚠️",
                        "title": "Anomaly Alert",
                        "text": f"Detected {outliers} outlier(s) in {col} ({pct:.1f}% of data) — values beyond 3 standard deviations",
                        "type": "anomaly"
                    })

        # 4. Correlation Analysis
        if len(numeric_cols) >= 2:
            corr = df[numeric_cols[:2]].corr().iloc[0, 1]
            if abs(corr) > 0.7:
                strength = "Strong" if abs(corr) > 0.8 else "Moderate"
                direction = "positive" if corr > 0 else "negative"
                insights.append({
                    "icon": "🔗",
                    "title": "Correlation Found",
                    "text": f"{strength} {direction} correlation ({corr:.2f}) between {numeric_cols[0]} and {numeric_cols[1]}",
                    "type": "trend"
                })

        # 5. Data Quality Assessment
        total_cells = df.shape[0] * df.shape[1]
        missing = df.isnull().sum().sum()
        completeness = ((total_cells - missing) / total_cells * 100)

        if completeness < 95:
            insights.append({
                "icon": "ℹ️",
                "title": "Data Quality Note",
                "text": f"Dataset is {completeness:.1f}% complete with {missing:,} missing values. Consider data cleaning.",
                "type": "anomaly"
            })
        else:
            insights.append({
                "icon": "✅",
                "title": "Data Quality Excellent",
                "text": f"Dataset is {completeness:.1f}% complete — high quality data ready for analysis",
                "type": "quality"
            })

        # 6. Summary Statistics Insight
        if numeric_cols:
            col = numeric_cols[0]
            mean_val = df[col].mean()
            median_val = df[col].median()
            skew = df[col].skew()

            if abs(mean_val - median_val) / (median_val if median_val != 0 else 1) > 0.2:
                skew_dir = "right" if skew > 0 else "left"
                insights.append({
                    "icon": "📊",
                    "title": "Distribution Insight",
                    "text": f"{col} shows {skew_dir}-skewed distribution (mean: {mean_val:.2f}, median: {median_val:.2f})",
                    "type": "pattern"
                })

    except Exception as e:
        print(f"Insight generation error: {e}")

    return insights if insights else [{
        "icon": "💡",
        "title": "Ready for Analysis",
        "text": "Upload more data or adjust filters to generate deeper insights",
        "type": "default"
    }]

def create_professional_chart(fig, title=""):
    """Apply professional styling to charts"""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(22,27,34,0.6)',
        font={'color': '#e6edf3', 'family': 'Inter, sans-serif'},
        height=380,
        margin=dict(l=56, r=32, t=56, b=56),
        title={
            'text': title,
            'font': {'size': 15, 'color': '#e6edf3', 'family': 'Inter'},
            'x': 0.02,
            'xanchor': 'left'
        },
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="#161b22",
            bordercolor="#30363d",
            font_size=12,
            font_family="Inter"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(48,54,61,0.5)',
            zeroline=False,
            tickfont=dict(color='#8b949e', size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(48,54,61,0.5)',
            zeroline=False,
            tickfont=dict(color='#8b949e', size=11)
        ),
        legend=dict(
            bgcolor='rgba(22,27,34,0.8)',
            bordercolor='#30363d',
            borderwidth=1,
            font=dict(color='#8b949e', size=11)
        )
    )
    return fig

def calculate_statistics(df, col):
    """Calculate comprehensive statistical measures"""
    values = df[col].dropna()
    return {
        "mean":     values.mean(),
        "median":   values.median(),
        "std":      values.std(),
        "min":      values.min(),
        "max":      values.max(),
        "q1":       values.quantile(0.25),
        "q3":       values.quantile(0.75),
        "range":    values.max() - values.min(),
        "variance": values.var(),
        "skewness": values.skew(),
        "kurtosis": values.kurtosis()
    }

def create_kpi_card(title, value, delta=None, icon="fa-chart-line", color="blue"):
    """Create premium glassmorphism KPI card"""
    icon_class = f"ds-kpi-icon-{color}"

    trend_component = None
    if delta is not None:
        trend_class = "ds-kpi-trend-up" if delta >= 0 else "ds-kpi-trend-down"
        trend_arrow = "↑" if delta >= 0 else "↓"
        trend_component = html.Div([
            html.Span(f"{trend_arrow} {abs(delta):.1f}%")
        ], className=f"ds-kpi-trend {trend_class}")

    formatted_value = f"{value:,.2f}" if isinstance(value, (int, float)) else str(value)

    return html.Div([
        # Corner glow orb
        html.Div(className="ds-kpi-card-glow"),

        # Top row: icon + trend
        html.Div([
            html.Div([
                html.I(className=f"fas {icon}")
            ], className=f"ds-kpi-icon {icon_class}"),
            trend_component if trend_component else html.Div()
        ], className="ds-kpi-top"),

        # Label
        html.Div(title, className="ds-kpi-label"),

        # Value
        html.Div(formatted_value, className="ds-kpi-value"),

        # Sparkline placeholder
        html.Div(className="ds-kpi-sparkline")

    ], className="ds-kpi-card animate-in")

# ===============================
# LAYOUT
# ===============================

app.layout = html.Div([

    # Toast Container
    html.Div(id="toast-container", className="toast"),

    # ─── NAVBAR ──────────────────────────────────────────────────────────────
    html.Nav(className="ds-navbar", children=[
        html.Div(className="ds-navbar-inner", children=[

            # Left: Brand
            html.Div(className="ds-brand", children=[
                html.Div(html.I(className="fas fa-gem"), className="ds-brand-icon"),
                html.Span("DataSphere", className="ds-brand-name"),
                html.Span("v2.0", className="ds-version-badge")
            ]),

            # Center: Status
            html.Div(className="ds-navbar-center", children=[
                html.Div([
                    html.Div(className="ds-status-dot"),
                    html.Span("Live Data")
                ], className="ds-live-badge"),
                html.Div([
                    html.I(className="fas fa-database", style={"marginRight": "0.3rem"}),
                    html.Span(id="navbar-data-indicator", children="No file loaded")
                ], className="ds-data-loaded-badge", id="navbar-data-badge", style={"display": "none"})
            ]),

            # Right: Actions + DateTime
            html.Div(className="ds-navbar-right", children=[
                html.Button([
                    html.I(className="fas fa-download"),
                    html.Span(" Export", className="ms-1")
                ], id="export-btn", className="ds-btn ds-btn-primary"),

                html.Button([
                    html.I(className="fas fa-chart-bar"),
                    html.Span(" Chart Builder", className="ms-1")
                ], id="chart-builder-toggle-btn", className="ds-btn ds-btn-ghost"),

                html.Button(
                    html.I(className="fas fa-cog"),
                    id="settings-btn", className="ds-btn ds-btn-icon"
                ),

                html.Button(
                    html.I(className="fas fa-question-circle"),
                    id="help-btn", className="ds-btn ds-btn-icon"
                ),

                html.Div(
                    datetime.now().strftime("%b %d, %Y"),
                    className="ds-datetime"
                ),

                # User info + logout
                html.Div(id="navbar-user-info", children=[
                    html.Div([
                        html.I(className="fas fa-user-circle", style={"marginRight": "0.4rem", "color": "#58a6ff"}),
                        html.Span(id="navbar-username", style={"fontSize": "0.8rem", "color": "#e6edf3", "fontWeight": "600"}),
                    ], style={"display": "flex", "alignItems": "center", "marginRight": "0.5rem"}),
                    html.A([
                        html.I(className="fas fa-sign-out-alt", style={"marginRight": "0.3rem"}),
                        "Sign Out"
                    ], href="/logout", style={
                        "fontSize": "0.78rem", "color": "#8b949e", "textDecoration": "none",
                        "padding": "0.35rem 0.75rem", "borderRadius": "6px",
                        "border": "1px solid #30363d", "transition": "all 0.2s",
                        "whiteSpace": "nowrap"
                    })
                ], style={"display": "flex", "alignItems": "center"})
            ])
        ])
    ]),

    # ─── MAIN CONTENT ─────────────────────────────────────────────────────────
    html.Div(style={"padding": "0 0 2rem"}, children=[

        dbc.Container(fluid=True, children=[

            # Upload Hero Section
            html.Div(id="upload-hero-section", className="ds-hero", children=[

                html.Div(className="ds-hero-content animate-in", children=[

                    html.Div([
                        html.I(className="fas fa-bolt", style={"marginRight": "0.4rem"}),
                        "Enterprise Analytics Platform"
                    ], className="ds-hero-eyebrow"),

                    html.H1("Upload Your Data,\nUnlock the Insights", className="ds-hero-title"),

                    html.P(
                        "Instantly transform raw CSV or Excel files into interactive dashboards "
                        "powered by AI-generated insights, statistical analysis, and professional visualizations.",
                        className="ds-hero-subtitle"
                    ),

                    # Upload zone
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div([
                            html.Div(
                                html.I(className="fas fa-cloud-upload-alt"),
                                className="ds-upload-icon-wrap"
                            ),
                            html.H3("Drag & Drop or Click to Upload", className="ds-upload-title"),
                            html.P("CSV, XLSX, XLS  •  Up to 50 MB", className="ds-upload-subtitle"),
                            html.Div([
                                html.Span([html.I(className="fas fa-file-csv me-1"), "CSV"], className="ds-format-pill"),
                                html.Span([html.I(className="fas fa-file-excel me-1"), "XLSX"], className="ds-format-pill"),
                                html.Span([html.I(className="fas fa-file-alt me-1"), "XLS"], className="ds-format-pill"),
                            ], className="ds-format-pills")
                        ], className="ds-upload-zone"),
                        multiple=False
                    ),

                    # Quick-load suggestions
                    html.Div([
                        html.P("SAMPLE DATASETS", className="ds-quick-load-label"),
                        html.Div([
                            html.Span([html.I(className="fas fa-users me-1"), "customers.xlsx"],
                                      className="ds-sample-chip"),
                            html.Span([html.I(className="fas fa-chart-line me-1"), "sales.xlsx"],
                                      className="ds-sample-chip"),
                            html.Span([html.I(className="fas fa-table me-1"), "sample_data.csv"],
                                      className="ds-sample-chip"),
                        ], className="ds-sample-chips")
                    ], className="ds-quick-load")
                ])
            ]),

            # ─── DASHBOARD (shown after upload) ──────────────────────────────
            html.Div(id="dashboard-main", style={"display": "none", "padding": "1.5rem 0"}, children=[

                dcc.Loading(type="circle", color="#58a6ff", children=[

                    # Dataset Info Banner
                    html.Div(id="dataset-info", className="mb-3"),

                    # Chart Builder (collapsible)
                    dbc.Collapse(
                        html.Div(id="chart-builder-section"),
                        id="chart-builder-collapse",
                        is_open=False
                    ),

                    # Tabs Navigation
                    html.Div(className="ds-tabs-wrapper", children=[
                        dbc.Tabs(id="main-tabs", active_tab="tab-overview", children=[
                            dbc.Tab(
                                label="📊  Overview",
                                tab_id="tab-overview",
                                children=html.Div(id="kpi-section", className="pt-3")
                            ),
                            dbc.Tab(
                                label="📈  Analytics",
                                tab_id="tab-analytics",
                                children=html.Div(id="charts-section", className="pt-3")
                            ),
                            dbc.Tab(
                                label="🔢  Statistics",
                                tab_id="tab-stats",
                                children=html.Div(id="statistics-section", className="pt-3")
                            ),
                            dbc.Tab(
                                label="🗄️  Data Explorer",
                                tab_id="tab-data",
                                children=html.Div(id="table-section", className="pt-3")
                            ),
                        ])
                    ]),

                    # Insights (persistent, above tabs on overview)
                    html.Div(id="insights-section"),
                ])
            ]),

            # ─── FOOTER ──────────────────────────────────────────────────────
            html.Div(className="ds-footer", children=[
                html.Div(className="ds-footer-grid", children=[

                    # Brand col
                    html.Div([
                        html.Div("DataSphere", className="ds-footer-brand-name"),
                        html.Div("Enterprise Analytics Platform v2.0", className="ds-footer-tagline"),
                    ]),

                    # Tech stack col
                    html.Div([
                        html.Div("BUILT WITH", className="ds-footer-section-title"),
                        html.Div([
                            html.Span("Dash", className="ds-tech-badge"),
                            html.Span("Plotly", className="ds-tech-badge"),
                            html.Span("Pandas", className="ds-tech-badge"),
                            html.Span("NumPy", className="ds-tech-badge"),
                            html.Span("SciPy", className="ds-tech-badge"),
                            html.Span("Bootstrap", className="ds-tech-badge"),
                        ], className="ds-tech-badges")
                    ]),

                    # Performance col
                    html.Div([
                        html.Div("PERFORMANCE", className="ds-footer-section-title"),
                        html.P(id="performance-stats",
                               style={"color": "var(--text-2)", "fontSize": "0.8rem"})
                    ])
                ])
            ])
        ])
    ]),

    # Store components
    dcc.Store(id='stored-data'),
    dcc.Store(id='filtered-data'),
    dcc.Store(id='column-types'),
    dcc.Store(id='file-loaded-flag', data=False),
], style={"background": "var(--bg)", "minHeight": "100vh"})


# ===============================
# CALLBACKS
# ===============================

# Toggle chart builder
@app.callback(
    Output("chart-builder-collapse", "is_open"),
    Input("chart-builder-toggle-btn", "n_clicks"),
    State("chart-builder-collapse", "is_open"),
    prevent_initial_call=True
)
def toggle_chart_builder(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


# Main dashboard update
@app.callback(
    [
        Output("dataset-info",         "children"),
        Output("chart-builder-section","children"),
        Output("kpi-section",          "children"),
        Output("insights-section",     "children"),
        Output("statistics-section",   "children"),
        Output("charts-section",       "children"),
        Output("table-section",        "children"),
        Output("performance-stats",    "children"),
        Output("stored-data",          "data"),
        Output("column-types",         "data"),
    ],
    Input("upload-data", "contents"),
    State("upload-data", "filename")
)
def update_dashboard(contents, filename):
    """Main callback — generates complete dashboard from uploaded file"""

    if contents is None:
        return [None] * 10

    start_time = datetime.now()

    # Parse data
    df = parse_contents(contents, filename)

    if df is None or df.empty:
        error = dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            "Error: Could not parse the file. Please upload a valid CSV or Excel file."
        ], color="danger", className="animate-in")
        return [error] + [None] * 9

    # Detect column types
    numeric_cols, categorical_cols, datetime_cols = detect_column_types(df)
    col_types = {
        "numeric":     numeric_cols,
        "categorical": categorical_cols,
        "datetime":    datetime_cols
    }

    # ── 1. DATASET INFO BANNER ───────────────────────────────────────────────
    info_card = html.Div([
        html.Div([
            html.I(className="fas fa-database",
                   style={"color": "var(--primary)", "fontSize": "1rem"}),
        ], style={"marginRight": "1rem"}),
        html.Div([
            html.Div("FILE", className="ds-info-banner-label"),
            html.Div(filename, className="ds-info-banner-value",
                     style={"color": "var(--primary)"})
        ], className="ds-info-banner-item"),
        html.Div(className="ds-info-sep"),
        html.Div([
            html.Div("ROWS", className="ds-info-banner-label"),
            html.Div(f"{len(df):,}", className="ds-info-banner-value",
                     style={"color": "var(--secondary)"})
        ], className="ds-info-banner-item"),
        html.Div(className="ds-info-sep"),
        html.Div([
            html.Div("COLUMNS", className="ds-info-banner-label"),
            html.Div(f"{len(df.columns)}", className="ds-info-banner-value",
                     style={"color": "var(--warning)"})
        ], className="ds-info-banner-item"),
        html.Div(className="ds-info-sep"),
        html.Div([
            html.Div("NUMERIC", className="ds-info-banner-label"),
            html.Div(f"{len(numeric_cols)}", className="ds-info-banner-value",
                     style={"color": "var(--info)"})
        ], className="ds-info-banner-item"),
        html.Div(className="ds-info-sep"),
        html.Div([
            html.Div("CATEGORICAL", className="ds-info-banner-label"),
            html.Div(f"{len(categorical_cols)}", className="ds-info-banner-value",
                     style={"color": "var(--purple)"})
        ], className="ds-info-banner-item"),
    ], className="ds-info-banner animate-in mb-3",
       style={"display": "flex", "alignItems": "center", "flexWrap": "wrap"})

    # ── 2. CUSTOM CHART BUILDER ──────────────────────────────────────────────
    chart_builder = html.Div([
        html.Div([
            html.Div([
                html.Div(className="ds-section-title-bar"),
                html.Span([
                    html.I(className="fas fa-chart-bar me-2"),
                    "Custom Chart Builder"
                ], className="ds-section-title-text")
            ], className="ds-section-title")
        ]),
        dbc.Row([
            dbc.Col([
                html.Label("X Axis", style={"color": "var(--text-2)", "fontSize": "0.8rem",
                                            "fontWeight": "600", "marginBottom": "0.4rem",
                                            "textTransform": "uppercase", "letterSpacing": "0.05em"}),
                dcc.Dropdown(
                    id="custom-x-axis",
                    options=[{"label": col, "value": col} for col in df.columns],
                    placeholder="Select X axis...",
                    value=df.columns[0] if len(df.columns) > 0 else None,
                    style={"color": "#000"}
                )
            ], md=3),
            dbc.Col([
                html.Label("Y Axis", style={"color": "var(--text-2)", "fontSize": "0.8rem",
                                            "fontWeight": "600", "marginBottom": "0.4rem",
                                            "textTransform": "uppercase", "letterSpacing": "0.05em"}),
                dcc.Dropdown(
                    id="custom-y-axis",
                    options=[{"label": col, "value": col} for col in numeric_cols] if numeric_cols else [],
                    placeholder="Select Y axis...",
                    value=numeric_cols[0] if numeric_cols else None,
                    style={"color": "#000"}
                )
            ], md=3),
            dbc.Col([
                html.Label("Chart Type", style={"color": "var(--text-2)", "fontSize": "0.8rem",
                                                "fontWeight": "600", "marginBottom": "0.4rem",
                                                "textTransform": "uppercase", "letterSpacing": "0.05em"}),
                dcc.Dropdown(
                    id="custom-chart-type",
                    options=[
                        {"label": "📊 Bar Chart",    "value": "bar"},
                        {"label": "📈 Line Chart",   "value": "line"},
                        {"label": "🔵 Scatter Plot", "value": "scatter"},
                        {"label": "📉 Area Chart",   "value": "area"},
                        {"label": "📊 Histogram",    "value": "histogram"},
                        {"label": "📦 Box Plot",     "value": "box"},
                        {"label": "🥧 Pie Chart",    "value": "pie"}
                    ],
                    placeholder="Select chart type...",
                    value="bar",
                    style={"color": "#000"}
                )
            ], md=3),
            dbc.Col([
                html.Label("Color By (Optional)", style={"color": "var(--text-2)", "fontSize": "0.8rem",
                                                         "fontWeight": "600", "marginBottom": "0.4rem",
                                                         "textTransform": "uppercase", "letterSpacing": "0.05em"}),
                dcc.Dropdown(
                    id="custom-color-by",
                    options=[{"label": col, "value": col} for col in categorical_cols] if categorical_cols else [],
                    placeholder="Select grouping...",
                    style={"color": "#000"}
                )
            ], md=3)
        ]),
        html.Hr(style={"borderColor": "var(--border)", "margin": "1.25rem 0"}),
        html.Div(id="custom-chart-output", className="mt-2")
    ], className="ds-builder-card animate-in")

    # ── 3. KPI CARDS ────────────────────────────────────────────────────────
    kpi_cards = []
    icon_map    = ["fa-chart-line", "fa-chart-bar", "fa-chart-pie", "fa-chart-area"]
    color_map   = ["blue", "green", "amber", "purple"]

    if numeric_cols:
        for i, col in enumerate(numeric_cols[:4]):
            mean_val = df[col].mean()
            std_val  = df[col].std()
            delta    = (std_val / mean_val * 100) if mean_val != 0 else 0
            kpi_cards.append(
                dbc.Col(
                    create_kpi_card(col, mean_val, delta,
                                    icon_map[i % len(icon_map)],
                                    color_map[i % len(color_map)]),
                    md=3, sm=6, className="mb-3"
                )
            )

    # AI Insights
    insights = generate_ai_insights(df, numeric_cols, categorical_cols, datetime_cols)

    insight_type_map = {
        "trend":   "ds-insight-trend",
        "pattern": "ds-insight-pattern",
        "anomaly": "ds-insight-anomaly",
        "quality": "ds-insight-quality",
        "default": "ds-insight-default"
    }

    insight_items = []
    for ins in insights:
        css_type = insight_type_map.get(ins.get("type", "default"), "ds-insight-default")
        insight_items.append(
            html.Div([
                html.Div(ins["icon"], className="ds-insight-icon-wrap"),
                html.Div([
                    html.Div(ins["title"], className="ds-insight-title"),
                    html.Div(ins["text"],  className="ds-insight-text")
                ], style={"flex": "1", "minWidth": 0})
            ], className=f"ds-insight-item {css_type}")
        )

    kpi_section = html.Div([
        # KPI Row
        html.Div([
            html.Div([
                html.Div(className="ds-section-title-bar"),
                html.Span([
                    html.I(className="fas fa-tachometer-alt me-2"),
                    "Key Performance Indicators"
                ], className="ds-section-title-text"),
                html.Span(f"{len(numeric_cols)} Metrics", className="ds-section-title-badge")
            ], className="ds-section-title"),
            dbc.Row(kpi_cards)
        ]) if kpi_cards else None,

        # Insights panel below KPIs in Overview tab
        html.Div([
            html.Div([
                html.Div(className="ds-section-title-bar"),
                html.Span([
                    html.I(className="fas fa-lightbulb me-2"),
                    "AI-Powered Insights"
                ], className="ds-section-title-text"),
                html.Span(f"{len(insights)} Discoveries", className="ds-section-title-badge")
            ], className="ds-section-title"),
            html.Div(insight_items, className="ds-insights-panel animate-in")
        ], style={"marginTop": "1.5rem"})

    ]) if kpi_cards else None

    # insights-section output (kept for compatibility, hidden—content now inside kpi_section)
    insights_section = None

    # ── 5. STATISTICS SECTION ───────────────────────────────────────────────
    stats_cards = []
    if numeric_cols:
        col = numeric_cols[0]
        sd = calculate_statistics(df, col)

        stat_items = [
            ("Mean",    sd["mean"],   "fa-calculator",   "blue"),
            ("Median",  sd["median"], "fa-chart-line",   "green"),
            ("Std Dev", sd["std"],    "fa-wave-square",  "amber"),
            ("Range",   sd["range"],  "fa-arrows-alt-h", "purple"),
        ]

        for label, value, icon, color in stat_items:
            stats_cards.append(
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.I(className=f"fas {icon}")
                        ], className=f"ds-stat-icon",
                           style={"background": f"rgba(88,166,255,0.1)", "color": "var(--primary)"}),
                        html.Div(label, className="ds-stat-label"),
                        html.Div(f"{value:,.2f}", className="ds-stat-value")
                    ], className="ds-stat-card animate-in")
                ], md=3, sm=6, className="mb-3")
            )

        # Extended stats table
        extended = [
            ("Q1 (25th pct)", sd["q1"]),
            ("Q3 (75th pct)", sd["q3"]),
            ("Variance",      sd["variance"]),
            ("Skewness",      sd["skewness"]),
            ("Kurtosis",      sd["kurtosis"]),
            ("Min",           sd["min"]),
            ("Max",           sd["max"]),
        ]

    statistics_section = html.Div([
        html.Div([
            html.Div(className="ds-section-title-bar"),
            html.Span([
                html.I(className="fas fa-chart-bar me-2"),
                f"Statistical Analysis — {numeric_cols[0] if numeric_cols else 'N/A'}"
            ], className="ds-section-title-text")
        ], className="ds-section-title"),
        dbc.Row(stats_cards),

        # Extended stats
        html.Div([
            html.Div([
                html.Div(className="ds-section-title-bar"),
                html.Span("Extended Statistics", className="ds-section-title-text")
            ], className="ds-section-title"),
            html.Div([
                html.Table([
                    html.Tbody([
                        html.Tr([
                            html.Td(label, style={"padding": "0.5rem 1rem", "color": "var(--text-2)",
                                                   "fontSize": "0.875rem", "fontWeight": "600",
                                                   "borderBottom": "1px solid var(--border)"}),
                            html.Td(f"{val:,.4f}", style={"padding": "0.5rem 1rem", "color": "var(--text-1)",
                                                          "fontSize": "0.875rem", "fontFamily": "monospace",
                                                          "borderBottom": "1px solid var(--border)"})
                        ]) for label, val in extended
                    ])
                ], style={"width": "100%", "borderCollapse": "collapse"})
            ], style={"background": "var(--surface)", "border": "1px solid var(--border)",
                      "borderRadius": "var(--radius-md)", "overflow": "hidden"})
        ], style={"marginTop": "1.5rem"}) if numeric_cols else None

    ]) if stats_cards else None

    # ── 6. CHARTS SECTION ───────────────────────────────────────────────────
    chart_components = []
    color_seq = ['#58a6ff', '#7ee787', '#e3b341', '#f85149', '#d2a8ff', '#79c0ff']

    # Distribution Histogram
    if numeric_cols:
        fig = px.histogram(df, x=numeric_cols[0], color_discrete_sequence=[color_seq[0]])
        fig = create_professional_chart(fig, f"Distribution of {numeric_cols[0]}")
        fig.update_traces(marker_line_width=1.5, marker_line_color='#1f6feb', opacity=0.88)
        chart_components.append(
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-chart-bar me-2",
                                   style={"color": "var(--primary)"}),
                            html.Span(f"Distribution — {numeric_cols[0]}", className="")
                        ], className="ds-chart-title"),
                        html.Span("HISTOGRAM", className="ds-chart-type-badge")
                    ], className="ds-chart-header"),
                    html.Div(
                        dcc.Graph(figure=fig, config={'displayModeBar': False}),
                        className="ds-chart-body"
                    )
                ], className="ds-chart-card")
            ], md=6)
        )

    # Category Analysis
    if categorical_cols and numeric_cols:
        cat_col = categorical_cols[0]
        num_col = numeric_cols[0]
        top_cats = df[cat_col].value_counts().head(10).index
        df_filtered = df[df[cat_col].isin(top_cats)]

        fig = px.bar(
            df_filtered.groupby(cat_col)[num_col].mean().reset_index(),
            x=cat_col, y=num_col, color_discrete_sequence=[color_seq[1]]
        )
        fig = create_professional_chart(fig, f"Avg {num_col} by {cat_col}")
        fig.update_traces(marker_line_width=1.5, marker_line_color='#238636')
        chart_components.append(
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-chart-column me-2",
                                   style={"color": "var(--secondary)"}),
                            html.Span("Category Analysis")
                        ], className="ds-chart-title"),
                        html.Span("BAR", className="ds-chart-type-badge",
                                  style={"color": "var(--secondary)",
                                         "background": "rgba(126,231,135,0.1)",
                                         "borderColor": "rgba(126,231,135,0.25)"})
                    ], className="ds-chart-header"),
                    html.Div(
                        dcc.Graph(figure=fig, config={'displayModeBar': False}),
                        className="ds-chart-body"
                    )
                ], className="ds-chart-card")
            ], md=6)
        )

    # Time Series
    if datetime_cols and numeric_cols:
        date_col = datetime_cols[0]
        num_col  = numeric_cols[0]
        df_time  = df.copy()
        df_time[date_col] = pd.to_datetime(df_time[date_col], format='mixed', errors='coerce')
        df_time = df_time.sort_values(date_col)

        fig = px.line(df_time, x=date_col, y=num_col, color_discrete_sequence=[color_seq[0]])
        fig = create_professional_chart(fig, f"{num_col} Over Time")
        fig.update_traces(line_width=3, fill='tozeroy', fillcolor='rgba(88,166,255,0.12)')
        chart_components.append(
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-chart-line me-2",
                                   style={"color": "var(--primary)"}),
                            html.Span("Time Series Analysis")
                        ], className="ds-chart-title"),
                        html.Span("LINE", className="ds-chart-type-badge")
                    ], className="ds-chart-header"),
                    html.Div(
                        dcc.Graph(figure=fig, config={'displayModeBar': False}),
                        className="ds-chart-body"
                    )
                ], className="ds-chart-card")
            ], md=12)
        )

    # Correlation Heatmap
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r', aspect='auto')
        fig = create_professional_chart(fig, "Correlation Matrix")
        fig.update_traces(textfont={"size": 11})
        chart_components.append(
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-table-cells me-2",
                                   style={"color": "var(--purple)"}),
                            html.Span("Correlation Analysis")
                        ], className="ds-chart-title"),
                        html.Span("HEATMAP", className="ds-chart-type-badge",
                                  style={"color": "var(--purple)",
                                         "background": "rgba(210,168,255,0.1)",
                                         "borderColor": "rgba(210,168,255,0.25)"})
                    ], className="ds-chart-header"),
                    html.Div(
                        dcc.Graph(figure=fig, config={'displayModeBar': False}),
                        className="ds-chart-body"
                    )
                ], className="ds-chart-card")
            ], md=12)
        )

    charts_section = html.Div([
        html.Div([
            html.Div(className="ds-section-title-bar"),
            html.Span([
                html.I(className="fas fa-chart-pie me-2"),
                "Data Visualizations"
            ], className="ds-section-title-text"),
            html.Span(f"{len(chart_components)} Charts", className="ds-section-title-badge")
        ], className="ds-section-title"),
        dbc.Row(chart_components, className="animate-in")
    ]) if chart_components else None

    # ── 7. DATA TABLE ───────────────────────────────────────────────────────
    table = dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.head(100).to_dict('records'),
        page_size=25,
        page_current=0,
        sort_action='native',
        sort_mode='multi',
        filter_action='native',
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign':       'left',
            'padding':         '10px 14px',
            'fontFamily':      'Inter, sans-serif',
            'backgroundColor': '#161b22',
            'color':           '#e6edf3',
            'border':          '1px solid #30363d',
            'fontSize':        '0.8rem'
        },
        style_header={
            'backgroundColor': '#0d1117',
            'fontWeight':      '700',
            'borderBottom':    '2px solid #58a6ff',
            'color':           '#e6edf3',
            'textTransform':   'uppercase',
            'fontSize':        '0.7rem',
            'letterSpacing':   '0.06em',
            'padding':         '10px 14px'
        },
        style_data_conditional=[
            {'if': {'row_index': 'odd'},
             'backgroundColor': '#161b22'},
            {'if': {'row_index': 'even'},
             'backgroundColor': '#0d1117'},
            {'if': {'state': 'active'},
             'backgroundColor': 'rgba(88,166,255,0.12)',
             'border': '1px solid #58a6ff'}
        ],
        export_format='xlsx',
        export_headers='display',
        style_as_list_view=True
    )

    table_section = html.Div([
        html.Div([
            html.Div(className="ds-section-title-bar"),
            html.Span([
                html.I(className="fas fa-table me-2"),
                "Data Explorer"
            ], className="ds-section-title-text"),
            html.Span(f"Showing top 100 of {len(df):,} rows", className="ds-section-title-badge")
        ], className="ds-section-title"),

        html.Div([
            html.Div([
                html.Div([
                    html.Span([
                        html.I(className="fas fa-circle me-1",
                               style={"color": "var(--secondary)", "fontSize": "0.5rem"}),
                        f"{len(df):,} total rows  •  {len(df.columns)} columns"
                    ], className="ds-row-badge"),
                    dbc.Button([
                        html.I(className="fas fa-file-excel me-2"),
                        "Export Excel"
                    ], color="primary", size="sm",
                       style={"background": "linear-gradient(135deg, #58a6ff, #79c0ff)",
                              "border": "none", "fontWeight": "600"})
                ], className="ds-table-header"),
                table
            ], className="ds-table-wrapper animate-in")
        ])
    ])

    # Performance stats
    elapsed   = (datetime.now() - start_time).total_seconds()
    mem_kb    = df.memory_usage(deep=True).sum() / 1024
    perf_stats = (
        f"{len(df):,} rows  •  {len(df.columns)} columns  •  "
        f"Loaded in {elapsed:.2f}s  •  {mem_kb:.1f} KB RAM"
    )

    # Store data
    stored = df.to_json(date_format='iso', orient='split')

    return (
        info_card, chart_builder, kpi_section, insights_section,
        statistics_section, charts_section, table_section,
        perf_stats, stored, col_types
    )


# Show/hide hero vs dashboard after upload
@app.callback(
    [
        Output("upload-hero-section", "style"),
        Output("dashboard-main",      "style"),
        Output("navbar-data-badge",   "style"),
        Output("navbar-data-indicator", "children"),
    ],
    Input("stored-data", "data"),
    prevent_initial_call=True
)
def toggle_sections(stored_data):
    if stored_data:
        return (
            {"display": "none"},
            {"display": "block", "padding": "1.5rem 0"},
            {"display": "flex"},
            "Data Loaded"
        )
    return (
        {"display": "flex", "flexDirection": "column", "alignItems": "center",
         "justifyContent": "center"},
        {"display": "none"},
        {"display": "none"},
        "No file loaded"
    )


# Custom chart builder callback
@app.callback(
    Output("custom-chart-output", "children"),
    [
        Input("custom-x-axis",    "value"),
        Input("custom-y-axis",    "value"),
        Input("custom-chart-type","value"),
        Input("custom-color-by",  "value"),
        Input("stored-data",      "data")
    ],
    prevent_initial_call=True
)
def update_custom_chart(x_col, y_col, chart_type, color_col, stored_data):
    """Update custom chart based on user selections"""

    if not stored_data or not x_col:
        return html.Div([
            html.I(className="fas fa-info-circle me-2",
                   style={"color": "var(--info)"}),
            "Select columns and chart type to generate your custom visualization"
        ], style={"color": "var(--text-2)", "padding": "2rem", "textAlign": "center"})

    try:
        df = pd.read_json(stored_data, orient='split')

        if chart_type == "bar":
            if y_col:
                fig = px.bar(df, x=x_col, y=y_col, color=color_col,
                             color_discrete_sequence=px.colors.sequential.Blues)
            else:
                fig = px.histogram(df, x=x_col, color=color_col,
                                   color_discrete_sequence=px.colors.sequential.Blues)
        elif chart_type == "line":
            fig = px.line(df, x=x_col, y=y_col, color=color_col,
                          color_discrete_sequence=px.colors.sequential.Blues)
            fig.update_traces(line_width=3)
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                             color_discrete_sequence=px.colors.sequential.Blues)
        elif chart_type == "area":
            fig = px.area(df, x=x_col, y=y_col, color=color_col,
                          color_discrete_sequence=px.colors.sequential.Blues)
        elif chart_type == "histogram":
            fig = px.histogram(df, x=x_col, color=color_col,
                               color_discrete_sequence=px.colors.sequential.Blues)
        elif chart_type == "box":
            fig = px.box(df, x=x_col, y=y_col, color=color_col,
                         color_discrete_sequence=px.colors.sequential.Blues)
        elif chart_type == "pie":
            if not color_col:
                fig = px.pie(df, names=x_col, values=y_col if y_col else None,
                             color_discrete_sequence=px.colors.sequential.Blues)
            else:
                fig = px.pie(df, names=color_col, values=y_col if y_col else None,
                             color_discrete_sequence=px.colors.sequential.Blues)
        else:
            fig = px.bar(df, x=x_col, y=y_col)

        title = f"Custom {chart_type.title()}: {y_col if y_col else x_col}"
        if color_col:
            title += f"  (by {color_col})"

        fig = create_professional_chart(fig, title)

        return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-magic me-2", style={"color": "var(--primary)"}),
                        html.Span(title)
                    ], className="ds-chart-title"),
                    html.Span(chart_type.upper(), className="ds-chart-type-badge")
                ], className="ds-chart-header"),
                html.Div(
                    dcc.Graph(figure=fig, config={'displayModeBar': True, 'displaylogo': False}),
                    className="ds-chart-body"
                )
            ], className="ds-chart-card")
        ])

    except Exception as e:
        return dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            f"Error creating chart: {str(e)}"
        ], color="warning")


# Export button callback
@app.callback(
    Output("toast-container", "children"),
    Input("export-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_export(n_clicks):
    if n_clicks:
        return dbc.Toast(
            [
                html.I(className="fas fa-info-circle me-2"),
                "Export ready! Use the 'Export Excel' button in the Data Explorer tab, or install kaleido for PDF export."
            ],
            header="Export Options",
            icon="info",
            duration=5000,
            style={"position": "fixed", "top": 80, "right": 20, "minWidth": "360px",
                   "background": "var(--surface-2)", "border": "1px solid var(--border)",
                   "color": "var(--text-1)"}
        )


# Help button callback
@app.callback(
    Output("toast-container", "children", allow_duplicate=True),
    Input("help-btn", "n_clicks"),
    prevent_initial_call=True
)
def show_help(n_clicks):
    if n_clicks:
        return dbc.Toast(
            [
                html.H6("🚀 Quick Start Guide", className="mb-2",
                        style={"color": "var(--text-1)", "fontWeight": "700"}),
                html.Ol([
                    html.Li("Upload your CSV or Excel file using the upload zone"),
                    html.Li("View auto-generated AI insights and KPI cards in Overview"),
                    html.Li("Explore charts in the Analytics tab"),
                    html.Li("Review statistics in the Statistics tab"),
                    html.Li("Sort, filter, and export data in Data Explorer"),
                    html.Li("Build custom charts using the Chart Builder button in the navbar"),
                ], className="mb-0", style={"fontSize": "0.85rem", "color": "var(--text-2)"})
            ],
            header="Help",
            icon="info",
            duration=10000,
            style={"position": "fixed", "top": 80, "right": 20, "minWidth": "400px",
                   "background": "var(--surface-2)", "border": "1px solid var(--border)",
                   "color": "var(--text-1)"}
        )


# Settings button callback
@app.callback(
    Output("toast-container", "children", allow_duplicate=True),
    Input("settings-btn", "n_clicks"),
    prevent_initial_call=True
)
def show_settings(n_clicks):
    if n_clicks:
        return dbc.Toast(
            [
                html.I(className="fas fa-cog me-2"),
                "Settings panel — Customize theme, display options, and export preferences. (Coming soon)"
            ],
            header="Settings",
            icon="secondary",
            duration=4000,
            style={"position": "fixed", "top": 80, "right": 20, "minWidth": "360px",
                   "background": "var(--surface-2)", "border": "1px solid var(--border)",
                   "color": "var(--text-1)"}
        )



# ===============================
# RUN APP
# ===============================
if __name__ == "__main__":
    import os
    print("\n" + "="*55)
    print("  🚀  DataSphere Enterprise Analytics Platform v2.0")
    print("="*55)
    print(f"  Landing Page  →  http://localhost:8080/")
    print(f"  Dashboard     →  http://localhost:8080/dashboard/")
    print(f"  Login         →  http://localhost:8080/login")
    print(f"  Register      →  http://localhost:8080/register")
    print("="*55 + "\n")
    if os.name == 'nt':
        app.run(debug=True, port=8080, use_reloader=False)
    else:
        app.run(debug=True, port=8080)
